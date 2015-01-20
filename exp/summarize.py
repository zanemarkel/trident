""" Get a summary of a single machine learning trial a single machine learning
trial. """
###############################################################
# Author:       Zane Markel
# Created:      20 FEB 2013
#
# Name:         trial
# Description:  Parses the output of trial.py and prints 
#               a line of csv
#
#               NOTE: the first line is a dict of the options, consider using 
#               import ast \n ast.literal_eval(line) in order to get it
#               
###############################################################

import argparse

def main():
    ''' Parse the results of a single machine learning trial
    Output is a line of csv. '''

    # Command line option Parser
    clparser = argparse.ArgumentParser()
    clparser.add_argument("results", type=file, \
            help='file containing a trial\'s results')
    clparser.add_argument("-c", "--comments", type=str, \
            help='comments to add to line')
    args = clparser.parse_args()

    summarize(args)

def summarize(args):
    ''' The function that actually does all the labor. '''

    # Parse the file for averages
    summary = ''
    with args.results as res:
        
        # The first line is a dict string
        _ = res.readline()
        # The next line in the header information
        _ = res.readline()

        # Make a line
        for line in res.readlines():
            linemod = line.strip().split()
            summary += '{}'.format(linemod[1]) + ','


        # Append the comments
        summary += '{}'.format(args.comments)

        # Output the csv line
        print(summary)

if __name__ == '__main__':
    main()
