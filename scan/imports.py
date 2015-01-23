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
    print(f, file=sys.stderr)
    pe = pefile.PE(f, fast_load=True)

    myimps = set()
    
    # Get the set of imported symbols
    pe.parse_data_directories()
    for entry in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', []):
        for imp in entry.imports:
            myimps.add(imp.name)
    
    return myimps

def main():
    ''' The main function.'''

    # Parse the CL args
    parser = argparse.ArgumentParser(description='Get the set of all imported \
            symbols from the files in a list of PE\'s.')
    parser.add_argument('fileList', type=argparse.FileType('r'), \
            default=sys.stdin, help='file containing list of PE files.')
    args = parser.parse_args()

    # Open up the list of files
    with args.fileList as files:

        _ = files.readline() # junk the header line

        # Maintain a file count for verbosity purposes
        finished = 0

        # The set of all imports
        tot_imps = set()

        # Read all the files
        for line in files.readlines():
            f = line.strip()
            tot_imps = tot_imps.union(getImps(f))
            finished += 1

            if (finished % 10000) == 0:
                print("{}".format(finished), file=sys.stderr)

        for imp in tot_imps:
            print(imp)

if __name__ == '__main__':
    main()
