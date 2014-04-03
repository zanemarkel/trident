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
    clparser.parse_args()

    # Parse the file

# Make a line

# Append the comments

# Output the csv line

if __name__ == '__main__':
    main()
