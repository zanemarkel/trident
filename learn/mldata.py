''' Library for data importation and feature selection'''
###############################################################################
# Author:       Zane Markel
# Created:      6 MAR 2014
#
# Name:         mldata
# Description : Library for importing/exporting data and feature selection
#
###############################################################################

# sklearn models can import svmlight files for data
# In general, sklearn uses the following data format:
# attributes X = n_samples vector of n_features feature vector
# labels Y = n_samples vector of class values

# scikit learn will provide most of the baseline funtionality
import numpy as np
import numpy.lib.recfunctions as rfunc
import random
import sys

# TODO: make it easy to import and export data
# check out numpy.recarray.tofile and .fromfile

def load_data(csv):
    ''' Import a csv file. Returns a structured array of the following format:
    [[name, feature0, ..., featuren, label], [name, ..., label], ...] 
    Note: "--" will be treated as a comment delimiter. I do not expect to use
    comments, but numpy.genfromtxt needs something.'''

    dformat = extract_headers(open(csv))

    # Load file data as a matrix
    data = np.genfromtxt(csv, delimiter=", ", dtype=dformat, skip_header=1, \
           comments='--')

    return data

def save_data(data, fname):
    ''' Takes a record array (like that returned by mldata.load_data) and
    saves it as a .csv file that could be imported by mldata.load_data. '''

    # Open file for writing:
    out = open(fname, 'w')
    
    # Get header names
    hnames = data.dtype.names

    # Print header names
    hline = ', '.join(hnames) + '\n'
    out.write(hline)

    # For every line in the array...
    for record in data:
        # Print that line
        # (Use list comprehension to get a string version of the record)
        recline = ', '.join((str(x) for x in record)) + '\n'
        out.write(recline)

    # For clarity
    return

def select_sample(seed, data, howmany, fractionMalware=-1):
    ''' Grabs a sample of data to use for learning. 
    
    seed = seed to use (so that sample can be reproduced)
    data = the large dataset to use.
    howmany = how many records to select.
    fractionMalware = percent of records (0 to 1) that will be malicious
                      default (-1) indicates no preference.'''

    # don't try to choose more records than there are in the data
    if(howmany >= len(data)):
        sys.stderr.write("SAMPLE IS ENTIRE DATASET!")
        return data

    # decide which record indices to pick
    random.seed(seed)
    if(fractionMalware == -1): # No preference for infected:clean ratio
        indices = random.sample(range(len(data)), howmany) 
    else:
        # get indices of malicious and benign records
        benind = np.where(data['isMalware'] == 0)[0]
        malind = np.where(data['isMalware'] == 1)[0]

        # get number of malicious and benign records that are requested
        nummal = int(round(fractionMalware * float(howmany)))
        numben = howmany - nummal

        # get samples of those indices
        # there's going to be an error if you ask for more than requested
        malind = random.sample(malind, nummal)
        benind = random.sample(benind, numben)

        # concatenate the sample indices together
        indices = malind + benind

        # Shuffle indices so that the malicious records do not come before the benign records
        random.shuffle(indices)

    # return only those record indices of data
    return data[indices]



def data_components(data):
    ''' Converts a structured array of data into simple arrays containing the
    features (2d array), labels, record names, and the feature names.
    This is intended to be used after preprocessing as the final step before
    doing the actual learning.'''
    
    # Get filenames
    recnames = data['Name']

    # Get labels
    labels = data['isMalware']

    # Get features
    features = rm_feat_name(data, 'Name')
    features = rm_feat_name(features, 'isMalware')
    featnames = features.dtype.names
    simplefeatures = features.view(np.int64).reshape(features.shape + (-1,))

    return (simplefeatures, labels, recnames, featnames)

def rm_feat_num(features, num):
    ''' Return features, with a feature removed based on column (num)ber '''
    names = list(features.dtype.names)
    new_names = names[:num] + names[num+1:]
    return features[new_names]
    
def rm_feat_name(features, name):
    ''' Return features, with a feature "name" removed'''
    names = list(features.dtype.names)
    if name in names:
        names.remove(name)
    return features[names]

def append_feat(data, name, fieldarray):
    ''' Appends fieldarray to data with the name 'name'. This allows new
    features to be added easily. 
    Because all new features will be built differently, it is up to you to 
    construct the fieldarray properly. 
    This is basically just a recast of numpy.lib.recfunctions.rec_append_fields
    , so that I do not have to look up the function again.'''

    return rfunc.rec_append_fields(data, name, fieldarray)

def extract_headers(openfile):
    ''' Extract the header line names and return a numpy.dtype for the
    dtype field of numpy.loadtxt''' 
    # for now just return the line as a string

    # Read the line
    headerline = openfile.readline()

    # Get the names
    nmes = headerline.strip().replace('"','').replace(' ','').split(',')

    # Generate types
    formats = ['i8']*len(nmes) # most entries will be 64-bit integers
    formats[nmes.index('Name')] = 'a255' # Name field will be a string

    # Generate dictionary 
    dtdict = {'names':tuple(nmes), 'formats':tuple(formats) }
    
    # Return numpy.dtype object
    return np.dtype(dtdict)
