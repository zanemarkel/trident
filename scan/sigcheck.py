''' Generate a feature list of whether a list of files has been sigchecked '''
# Zane Markel
# Created 29 sep 14
# Bilzor's source: https://github.com/hiddenillusion/AnalyzePE/blob/master/AnalyzePE.py

import subprocess
import argparse
import get_names

wine = 'wine' # change if wine is ever not in the path
# VVV this must be changed for your individual computer VVV
sigcheck = '/home/markel/sigcheck.exe' 

def sigchecker(fname):

    opts = " -q -a "
    cmd = wine + ' ' + sigcheck + opts + '"' + fname + '"'
    p = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
    (stdout, stderr) = p.communicate()
    if stdout:
        # Generate a string for the database
        retstr = '{}, {}, {}'.format(fname,get_isSigned(stdout), \
            get_entropy(stdout))
        print retstr
        return retstr
    else: 
        print stderr
        return None

def get_isSigned(stdout):
    ''' Searches through a report from sigcheck.exe and returns whether the
    file has been signed plus the PE entropy '''
    report = stdout.strip().split('\n')
    for line in report:
        if 'Verified:' in line:
            if 'Unsigned' in line: 
                return 0 # the file is not signed
            return 1 # the file is signed
    return 'ERROR'

def get_entropy(stdout):
    ''' Takes a sigcheck.exe report string and returns the PE entropy '''
    report = stdout.strip().split('\n')
    for line in report:
        if 'Entropy' in line:
            # split on the tab, and the last value will be the entropy
            entropy = line.strip().split('\t')[-1]

            # Round entropy and convert it to an int for scikit-learn's sake
            return int(round(float(entropy)))
    return 'ERROR'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('db', help='csv database')
    parser.add_argument('outfile', type=argparse.FileType('w'), \
        help='File to write to')
    parser.add_argument('--header', action='store_true', \
        help='Whether or not to output a csv header line')
    args = parser.parse_args()

    # If requested by args.header, write a csv header line
    if args.header:
        args.outfile.write('Name, isSigned, totalEntropy\n')

    fnames = get_names.names(args.db)
    for fname in fnames:
        report = sigchecker(fname)
        if report:
            args.outfile.write('{}\n'.format(report))


if __name__ == '__main__':
    main()
