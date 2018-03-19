#!/usr/bin/env python3
import argparse

import lib.parser



def main(args):
    mzml = lib.parser.MZMLParser(args.file_path)
    
    count = 0

    for record in mzml.iterate:
        if record.ms_level == '2':
            count += 1
    print(count)




def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args = get_arguments()
    main(args)
