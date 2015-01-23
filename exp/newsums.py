""" Get a summary of a single machine learning trial a single machine learning
trial. This summary will also calculate the average abs tp, fp, tn, and fn's."""
###############################################################
# Author:       Zane Markel
# Created:      20 JAN 2013
#
# Name:         newsums
# Description:  Parses the output of trial.py and prints 
#               a line of csv
#
#               NOTE: the first line is a dict of the options, consider using 
#               import ast \n ast.literal_eval(line) in order to get it
#               
###############################################################

import argparse
import re

def main():
    ''' Parse the results of a single machine learning trial
    Output is a line of csv. '''

    # Command line option Parser
    clparser = argparse.ArgumentParser()
    clparser.add_argument("results", nargs='?', type=file, \
            help='file containing a trial\'s results. If none specified, only \
            a header line will be printed.')
    clparser.add_argument("-c", "--comments", type=str, \
            help='comments to add to line')
    clparser.add_argument("--header", default=False, \
            action='store_true', help='Print the header line. (Default is to \
            not print header data when [results] is specified.)')
    args = clparser.parse_args()

    if(args.results):
        summarize(args)
    else:
        header()

def mine(res):
    ''' Reads relevant values from the 'res' results file into a dict. '''

    data = {}

    # First get the relevant parameters:
    # mp_tr, mp_te, numsamples
    params = res.readline()
    matchln = r"algorithm='(.+?)', .+ malfrac=\[(.+), (.+)\], numsamples=(.+),"
    match = re.search(matchln, params)
    data['algorithm'] = match.group(1)
    data['mp_tr'] = float(match.group(2))
    data['mp_te'] = float(match.group(3))
    data['numsamples'] = float(match.group(4))

    # Get the beta, too
    data['beta'] = 1.0
    matchln = r"beta=(.+?),"
    match = re.search(matchln, params)
    if(match):
        data['beta'] = float(match.group(1))

    # The next line in the header information
    _ = res.readline()

    # Get all the average perfmeasures
    for line in res.readlines():
        linemod = line.strip().split()
        if(linemod[0][0] == 'f'):
            linemod[0] = 'fbeta'
        data[linemod[0]] = float(linemod[1])

    return data

def analyze(data):
    ''' Take a data dict from mine() and return it with tp, fp, etc. 
    Note: these metrics are averages over all trials. Also, they are rounded
    for clarity.'''
    data['tp'] = round(data['recall'] * data['mp_te'] * data['numsamples'], 1)
    data['fn'] = round(data['mp_te'] * data['numsamples'] - data['tp'], 1)
    if data['precision'] != 0:
        data['fp'] = round(data['tp'] / data['precision'] - data['tp'], 1)
        data['tn'] = round(data['numsamples'] - data['tp'] - data['fp'] - \
                data['fn'], 1)
    else:
        data['fp'] = 'unk'
        data['tn'] = 'unk'

    return data

def header():
    ''' Print the header line. '''
    print 'tp, fp, tn, fn, p, r, fbeta, beta, mp_tr, mp_te, alg'


def summarize(args):
    ''' Gathers data and prints it in a csv format.
    Order = tp, fp, tn, fn, p, r, fbeta, beta, mp_tr, mp_te, alg'''

    # Parse the file for averages
    summary = ''
    with args.results as res:

        # Get the data
        data = mine(res)
        data = analyze(data)

        # (optionally) print the header line
        if(args.header):
            header()

        # Create the data string
        summary = '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(\
                data['tp'], data['fp'], data['tn'], data['fn'], \
                data['precision'], data['recall'], data['fbeta'], data['beta']\
                , data['mp_tr'], data['mp_te'], data['algorithm'])
        print summary
        
if __name__ == '__main__':
    main()
