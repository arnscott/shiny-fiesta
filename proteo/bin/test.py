#!/usr/bin/env python3
import argparse

import lib.parser



def main(args):
    mzid = lib.parser.MZIDParser(args.file_path)
    
    test_list = []

    for thing in mzid.iterate:
        test_list.append(thing)
 
    print(len(test_list))
    

    for thing in test_list:
        filtered_list = []
        for othing in thing.spectrum_items:
            for key, value in othing.items():
                print(key)
            if float(othing.QValue) <= 0.01:
                filtered_list.append(othing)
        thing.spectrum_items = filtered_list
                




def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args = get_arguments()
    main(args)
