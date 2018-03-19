from lxml import etree
from bs4 import BeautifulSoup



class SpectrumIdentificationResult(object):


    def __init__(self, element):
        attr_dict = {key: value for key, value in element.items()}    
        self.spectrum_id = attr_dict['spectrumID']
        self.spectra_data_ref = attr_dict['spectraData_ref']
        self.result_id = attr_dict['id']
        self.spectrum_items = []

    def add_items(self, elements):
        attr_dict = {}
        for element in elements:
            attr_dict = {key: value for key, value in element.items()}
            children = element.getchildren()
            for item in children:
                if item.tag == '{http://psidev.info/psi/pi/mzIdentML/1.1}cvParam':
                    for key, value in item.items():
                        if key == 'name':
                            attribute = value.split(':')[-1]
                        if key == 'value':
                            attr_dict[attribute] = float(value)
            self.spectrum_items.append(SpectraAttributes(attr_dict))




class MZIDParser(object):


    spectrum_result_tag = '{http://psidev.info/psi/pi/mzIdentML/1.1}SpectrumIdentificationResult'
    spectrum_id_item_tag = '{http://psidev.info/psi/pi/mzIdentML/1.1}SpectrumIdentificationItem'

    def __init__(self, file_path):
        self.file_path = file_path


    @property
    def iterate(self):
        with open(self.file_path, 'rb') as mzid:
            for event, element in etree.iterparse(mzid):
                if element.tag == self.spectrum_result_tag:
                    result = SpectrumIdentificationResult(element)
                    spec_items = element.findall(self.spectrum_id_item_tag)
                    result.add_items(spec_items)
                    yield result



class SpectraAttributes(object):
    def __init__(self, raw):
        self.id = raw['id']
        self.spec_e_value = raw['SpecEValue']
        self.pep_q_value = raw['PepQValue']
        self.e_value = raw['EValue']
        self.q_value = raw['QValue']
        self.de_novo_score = raw['DeNovoScore']
        self.raw_score = raw['RawScore']
        self.calculated_mass_to_charge = raw['calculatedMassToCharge']
        self.charge_state = raw['chargeState']
        self.experimental_mass_to_charge = raw['experimentalMassToCharge']
        self.pass_threshold = raw['passThreshold']
        self.peptide_ref = raw['peptide_ref']
        self.rank = raw['rank']

    def as_dict(self):
        return self.__dict__




class MZMLAttributes(object):

    def __init__(self, raw):
        self.index = raw['index']
        self.id = raw['id']
        self.default_array_length = raw['defaultArrayLength']
        self.ms_level = raw['ms level']
        if 'MS1 spectrum' in raw:
            self.msn_spectrum = raw['MS1 spectrum']
        else:
            self.msn_spectrum = raw['MSn spectrum']
        self.positive_scan = raw['positive scan']
        self.centroid_spectrum = raw['positive scan']
        self.base_peak_mz = raw['base peak m/z']
        self.base_peak_intensity = raw['base peak intensity']
        self.total_ion_current = raw['total ion current']
        self.lowest_observed_mz = raw['lowest observed m/z']
        self.highest_observed_mz = raw['highest observed m/z']
        if self.ms_level == '2':
            self.precursor_list = []



class MZMLParser(object):
    
    spectrum_tag = '{http://psi.hupo.org/ms/mzml}spectrum'
    cv_param_tag = '{http://psi.hupo.org/ms/mzml}cvParam'
    precursor_list_tag = '{http://psi.hupo.org/ms/mzml}precursorList'
    precursor_tag = '{http://psi.hupo.org/ms/mzml}precursor'

    def __init__(self, file_path):
        self.file_path = file_path

    @property
    def iterate(self):
        with open(self.file_path, 'rb') as mzml:
            for event, element in etree.iterparse(mzml):
                if element.tag == self.spectrum_tag:
                    attr_dict = {}
                    attr_dict = {key: value for key, value in element.items()}
                    cv_params = element.findall(self.cv_param_tag)
                    for cv_param in cv_params:
                        for key, value in cv_param.items():
                            if key == 'name':
                                attribute = value
                            if key == 'value':
                                attr_dict[attribute] = value
                    record = MZMLAttributes(attr_dict)
                    if record.ms_level == '2':
                        precursor_list = element.find(self.precursor_list_tag)
                        precursors = precursor_list.findall(self.precursor_tag)
                        for precursor in precursors:
                            record.precursor_list.append(precursor.get('spectrumRef'))
                    yield record
