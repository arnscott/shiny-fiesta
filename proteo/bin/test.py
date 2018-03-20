#!/usr/bin/env python3
import argparse
import csv


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
    features = []
    for row in iter_features_tsv(file_path):
        features.append(row)
    return features



def build_time_windows(scans):
    scan_dict = {}
    for index, scan in enumerate(scans):
        try:
            scan.scan_end = scans[index + 1].scan_time
        except IndexError:
            scan.scan_end = 'end'
        scan_dict[scan.id] = scan
    return scan_dict




def split_ms_levels(mzml):
    ms1_scans = []
    ms2_scans = []
    for scan in mzml.iterate:
        if scan.ms_level == '1':
            ms1_scans.append(scan)
        if scan.ms_level == '2':
            ms2_scans.append(scan)
    return ms1_scans, ms2_scans



def index_by_start_time(features):
    feature_dict = {}
    for feature in features:
        if not feature['rtStart'] in feature_dict:
            feature_dict[feature['rtStart']] = []
            feature_dict[feature['rtStart']].append(feature)
        else:
            feature_dict[feature['rtStart']].append(feature)
    return feature_dict




def main(args):
    mzml = lib.parser.MZMLParser(args.mzml_path)

    ms1_scans, ms2_scans = split_ms_levels(mzml)
    
    ms1_scans = build_time_windows(ms1_scans)

    for scan in ms2_scans:
        for key, value in scan.precursors.items():
            if key in ms1_scans:
                ms1_scans[key].ms2_scans.append(scan)
    


    features = index_by_start_time(parse_features_tsv(args.features_path))
    

    print(len(ms1_scans))
    print(len(ms2_scans))
    print(len(features))
    
    for scan_id, scan in ms1_scans.items():
        start_time = float(scan.scan_time)
        try:
            end_time = float(scan.scan_end)
        except ValueError as e:
            if scan.scan_end == 'end':
                end_time = start_time + 10000
            else:
                raise e
        remove_keys = []
        for key, value in features.items():
            rt_start = float(key)
            if rt_start >= start_time and rt_start < end_time:
                scan.features += value
                remove_keys.append(key)
        for key in remove_keys:
            features.pop(key)


    peptides = parse_peptides(args.peptide_path)
    
    for scan_id, scan in ms1_scans.items():
        for ms2_scan in scan.ms2_scans:
            if ms2_scan.id in peptides:
                ms1_scans[scan_id].peptides.append(peptides[ms2_scan.id])
    
        
    #for scan_id, scan in ms1_scans.items():
    #    print(scan.index, len(scan.features), len(scan.ms2_scans), len(scan.peptides))
    
    for scan_id, scan in ms1_scans.items():
        for feature in scan.features:
            feature_dict = {}
            for ms2_scan in scan.ms2_scans:
                for key, value in ms2_scan.precursors.items():
                    if float(feature['mz']) < (float(ms2_scan.precursors[key]) + 0.05) \
                            and float(feature['mz']) > (float(ms2_scan.precursors[key]) - 0.05):
                        feature_dict['feature mz'] = feature['mz']
                        feature_dict['ms2 ion mz'] = ms2_scan.precursors[key]
                        
                


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
