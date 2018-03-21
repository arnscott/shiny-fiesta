#!/usr/bin/env python3
import argparse
import csv
import math


import lib.parser





def parse_peptides(file_path):
    pep_dict = {}
    with open(file_path) as pepfile:
        reader = csv.DictReader(pepfile, delimiter='\t')
        for row in reader:
            pep_dict[row['SpecID']] = row
    return pep_dict


def iter_features_tsv(file_path):
    with open(file_path) as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:
            yield row


def parse_features_tsv(file_path):
    features = {}
    for row in iter_features_tsv(file_path):
        charge = row['charge']
        if not charge in features:
            features[charge] = []
        features[charge].append(row)
    for charge in features:
        features[charge].sort(key=lambda x: float(x['mz']))
    return features


def get_ms2_scans(mzml):
    ms2_scans = []
    for scan in mzml.iterate:
        if scan.ms_level == '2':
            ms2_scans.append(scan)
    return ms2_scans



def group_peptides(scans, peptides):
    scan_list = []
    for scan in scans:
        if scan.id in peptides:
            scan.add_peptide(peptides[scan.id])
            scan_list.append(scan)
    return scan_list



def group_scans(scans):
    scan_dict = {}
    for scan in scans:
        charge_state = scan.charge_state
        if not charge_state in scan_dict:
            scan_dict[charge_state] = []
        scan_dict[charge_state].append(scan)
    for charge in scan_dict:
        scan_dict[charge].sort(key=lambda x: float(x.mz))
    return scan_dict



def search_list_for_mz(scan_list, feature_mz):
    
    feature_mz = round(feature_mz)

    first = 0
    last = len(scan_list) - 1

    if len(scan_list) < 100:
        return scan_list
    else:
        i = (first + last) // 2
        scan_mz = scan_list[i].mz
        threshold = scan_list[i].threshold
        if scan_mz + threshold < feature_mz:
            search_list_for_mz(scan_list[i+1:], feature_mz)
        else:
            search_list_for_mz(scan_list[:i], feature_mz)




def main(args):
    mzml = lib.parser.MZMLParser(args.mzml_path)

    scans = get_ms2_scans(mzml)

    features = parse_features_tsv(args.features_path)


    scans = group_peptides(scans, 
                           parse_peptides(args.peptide_path))

    scans = group_scans(scans)


    for charge, scan_list in scans.items():
        print(charge, len(scan_list))

    print('features') 
    for charge, feature_list in features.items():
        print(charge, len(feature_list))

    output_fieldnames = ['feature_mz',
                         'ms2_scan_mz',
                         'charge',
                         'peptide',
                         'mzml_id']
    
    records = []

    for charge, feature_list in features.items():
        for feature in feature_list:
            feature_mz = float(feature['mz'])
            if charge in scans:
                scan_list = scans[charge]
                if scan_list:
                    for scan in scan_list:
                        scan_mz = scan.mz
                        if abs(feature_mz - scan_mz) <= scan.threshold:
                            record = {'feature_mz': feature_mz,
                                      'ms2_scan_mz': scan_mz,
                                      'charge': charge,
                                      'peptide':  scan.peptide['Peptide'],
                                      'mzml_id': scan.id}
                            records.append(record)

                        
    
    with open('gt3outfile', 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=output_fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)


                


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('mzml_path')
    parser.add_argument('features_path')
    parser.add_argument('peptide_path')
    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args = get_arguments()
    main(args)
