from lxml import etree


class Scan(object):

    def __init__(self):
        self.id = ''
        self.ms_level = ''
        self.peptide = {}
        self.features = []


    def set_precursor_values(self, attr_dict):
        self.mz = float(attr_dict['selected ion m/z'])
        self.charge_state = attr_dict['charge state']


    def add_peptide(self, peptide):
        self.peptide = peptide
        error = float(peptide['PrecursorError(ppm)'])
        precursor_mz = float(peptide['Precursor'])
        self.threshold = error / precursor_mz

    def add_precursor_scan_info(self, attr_dict):
        self.scan_start_time = float(attr_dict['scan start time'])


class MZMLParser(object):
    
    spectrum_tag = '{http://psi.hupo.org/ms/mzml}spectrum'
    cv_param_tag = '{http://psi.hupo.org/ms/mzml}cvParam'
    precursor_list_tag = '{http://psi.hupo.org/ms/mzml}precursorList'
    precursor_tag = '{http://psi.hupo.org/ms/mzml}precursor'
    scan_list_tag = '{http://psi.hupo.org/ms/mzml}scanList'
    scan_tag = '{http://psi.hupo.org/ms/mzml}scan'
    selected_ion_list_tag = '{http://psi.hupo.org/ms/mzml}selectedIonList'
    selected_ion_tag = '{http://psi.hupo.org/ms/mzml}selectedIon'

    def __init__(self, file_path):
        self.file_path = file_path

    
    @classmethod
    def parse_cv_params(cls, element):
        attr_dict = {}
        cv_params = element.findall(cls.cv_param_tag)
        for cv_param in cv_params:
            for key, value in cv_param.items():
                if key == 'name':
                    attribute = value
                elif key == 'value':
                    attr_dict[attribute] = value
        return attr_dict

    @property
    def iterate(self):
        with open(self.file_path, 'rb') as mzml:
            for event, element in etree.iterparse(mzml):
                if element.tag == self.spectrum_tag:
                    record = Scan()
                    attr_dict = {key: value for key, value in element.items()}
                    spectrum_cv_params = self.parse_cv_params(element)
                    attr_dict.update(spectrum_cv_params)
                    record.id = attr_dict['id']
                    record.ms_level = attr_dict['ms level']
                    if record.ms_level == '2':
                        precursor_list = element.find(self.precursor_list_tag)
                        precursors = precursor_list.findall(self.precursor_tag)
                        for precursor in precursors:
                            pre_key = precursor.get('spectrumRef')
                            selected_ion_list = precursor.find(self.selected_ion_list_tag)
                            selected_ion = selected_ion_list.find(self.selected_ion_tag)
                            ion_attr_dict = self.parse_cv_params(selected_ion)
                            record.set_precursor_values(ion_attr_dict)
                    scan_list_element = element.find(self.scan_list_tag)
                    scan_element = scan_list_element.find(self.scan_tag)
                    scan_dict = self.parse_cv_params(scan_element)
                    record.add_precursor_scan_info(scan_dict)
                    yield record
