''' Library for data importation and feature selection'''
###############################################################################
# Author:       Zane Markel
# Created:      6 MAR 2014
#
# Name:         mldata
# Description : Library for data importation and feature selection
#
###############################################################################

# sklearn models can import svmlight files for data
# In general, sklearn uses the following data format:
# attributes X = n_samples vector of n_features feature vector
# labels Y = n_samples vector of class values

# scikit learn will provide most of the baseline funtionality
import sklearn as sk
import numpy as np
import re

def csv2matrix(csvfile, mfile, namefile):
    ''' A function for converting a .csv file to a matrix file for numpy.
    Output is in the following format:
    <feature>, <feature>, ... , <label>
    where all features and the label are ints

    This function also writes a name-ID translation table, because each filename
    is converted into an ID.'''

    with open(csvfile) as csv:
        # Cut header data
        junk = extract_headers(csv)
        
        # Initial Setup
        mat = open(mfile, 'w') # the file to write the matrix to
        names = open(namefile, 'w') # the ID-fname translation file
        cnt = 0

        for line in csv:
            # Output ID-filename translation file
            thisname = re.match(r'^"(.+?)"', line)
            idline = str(cnt) + ' ' + str(thisname.group(1)) + '\n'
            names.write(idline)

            # Translate filenames to IDs
            newline = re.sub(r'^"(.+?)"', str(cnt), line)

            # replace True and malware with 1, and False and clean with 0
            newline = newline.replace('True','1').replace('malware','1')
            newline = newline.replace('False','0').replace('clean','0')

            # replace none with -1
            newline = newline.replace('None','-1')

            # Remove quotes
            newline = newline.replace('"','')

            # Output matrix file line
            mat.write(newline)

            # increase the count for the ID
            cnt += 1



def load_data(matrixf):
    ''' Import a matrix file. Returns a feature matrix and a label vector.''' 

    matrix = open(matrixf)

    # Load file data as a matrix
    data = np.loadtxt(matrix, dtype=int, delimiter=',')
    
    # Remove unwanted features (this will come later)

    # Get features
    features = data[:, :-1]

    # Get labels
    labels = data[:, -1]

    return (features, labels)
    

def extract_headers(openfile):
    ''' Get the header line data ''' 
    # for now just return the line as a string
    return openfile.readline()
