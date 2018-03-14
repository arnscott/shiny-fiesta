#!/usr/bin/env python3
import argparse

import lib.parser


def count_ms2(file_path):
    count = 0
    mzml = lib.parser.MZMLParser(file_path)
    for level in mzml.iterate:
        if level == '2':
            count += 1
    return count



def main(args):
    ms2_count = count_ms2(args.mzml_file)



def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('mzml_file')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_arguments()
    main(args)

