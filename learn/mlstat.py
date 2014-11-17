''' mlstat, or machine learning statistics, module used to easily do
statistical analysis on a machine learning trial'''
###############################################################################
# Author:       Zane Markel
# Created:      23 MAR 2014
#
# Name:         mlstat
# Description:  contains various functions for easily running machine learning 
#               trial result analysis
#
###############################################################################

import numpy as np

def acc(pred, true):
    ''' computes the accuracy of a trial (from 0 to 1)
    pred = array of predicted labels
    true = array of true labels '''

    # Get the correct and the total number of predictions
    corr = np.sum(np.array(pred) == np.array(true))
    tot = len(pred)

    return float(corr) / float(tot)

def print_results_header():
    ''' standard output file header '''
    print('  Measure  Average   StdDev Fold-Scores')

def printresults(perfmeasure, scores):
    ''' Prints a standard string summarizing several scores. '''
    # Print the results
    avgstr = '{:.4f}'.format(scores.mean()).rjust(9)
    stdstr = '{:.4f}'.format(scores.std()).rjust(9)
    resultstr = '{}{}{} '.format(perfmeasure.rjust(9), avgstr, stdstr)
    for score in scores:
        resultstr += ' {:.3}'.format(score)
    print(resultstr)
    return

