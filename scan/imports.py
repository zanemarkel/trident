from __future__ import print_function

''' Print the set of all imports in all of the files in a given list of pe    
files. '''

###############################################################
# Author:       Zane Markel
# Created:      22 JAN 2015
#
# Name:         imports
# Description:  See docstring above
#
###############################################################

import pefile
import argparse
import sys

def getImps(f):
    ''' Return the set of imports in the given file. '''
    pe = pefile.PE(f, fast_load=True)

    myimps = set()
    
    # Get the set of imported symbols
    pe.parse_data_directories()
    
    # getattr prevents a crash when a pe doesn't have any imports.
    for entry in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', []):
        for imp in entry.imports:
            myimps.add(imp.name)
    
    return myimps

def feature_line(label, name, imps):
    ''' Returns a csv line perfectly formatted for isMalware, Name, <imps>'''
    feats = []

    # Add the label
    if('malicious' == label):
        feats.append('1')
    else:
        feats.append('0')

    # Add the filename
    feats.append(name)

    # Get the list of imported symbols for the file
    rawimps = getImps(name)

    # Add binary feature values for each feature in imps
    for imp in imps:
        if imp in rawimps:
            feats.append('1')
        else:
            feats.append('0')

    return ', '.join(feats)

def header_line(imps):
    ''' The header line, which is printed unless --append is chosen. '''
    print('isMalware, Name, {}'.format(', '.join(imps)))

def main():
    ''' The main function.'''

    # Parse the CL args
    parser = argparse.ArgumentParser(description='Get the set of all imported \
            symbols from the files in a list of PE\'s.')
    parser.add_argument('fileList', type=argparse.FileType('r'), \
            default=sys.stdin, help='file containing list of PE files.')
    parser.add_argument('imports', type=argparse.FileType('r'), \
            help='file containing list of import symbols to use as features.')
    parser.add_argument('label', choices=['malicious', 'benign'], \
            help='whether the given files are benign or malicious.')
    parser.add_argument('--noheader', action='store_true', default=False, \
            help='Do not write a header line.')
    args = parser.parse_args()

    # Get the list of features
    imps = []
    with args.imports as impsFile:
        imps = impsFile.readlines()
        imps = [imp.strip() for imp in imps]

    # Write a header line, if necessary
    if(not args.noheader):
        header_line(imps)
   
    # Open up the list of files
    with args.fileList as files:

        # Maintain a file count for verbosity purposes
        finished = 0

        # Read all the files
        for line in files.readlines():
            f = line.strip()

            # Generate and print the csv line
            line = feature_line(args.label, f, imps)
            print(line)

            # For verbosity purposes
            finished += 1
            if (finished % 1000) == 0:
                print("Finished {} {}".format(finished, args.label), \
                        file=sys.stderr)

if __name__ == '__main__':
    main()
