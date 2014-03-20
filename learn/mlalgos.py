''' mlalgos, or machine learning algorithms, is a library for easily using 
various machine learning algorithms'''
###############################################################################
# Author:       Zane Markel
# Created:      6 MAR 2014
#
# Name:         mlalgos
# Description:  contains various functions for easily running machine learning 
#               algorithms
#
###############################################################################

# scikit learn will provide most of the baseline funtionality
from sklearn.naive_bayes import GaussianNB


###############################################################################
# WRAPPER FUNCTIONS
###############################################################################

# This function will be used to learn using an arbitrary algorithm
def learn(algoname, trainx, trainy):
    '''
Learn using an arbitrary algorithm. The choices for algoname are:
nb = Naive Bayes
'''
    if(algoname == 'nb'):
        return nb_fit(trainx, trainy)

    # You only get here if the string was invalid
    print("Unrecognized algorithm name")
    return

# Make predictions using a model
def predict(model, testx):
    ''' Make predictions using a model generated from the learn function.'''
    if( isinstance(model, GaussianNB)):
        return nb_predict(model, testx) 
    else:
        print("Unrecognized model")
        return

###############################################################################
# NAIVE BAYES
###############################################################################

# NB fit on data
# Returns a GaussianNB.fit object
def nb_fit(trainx, trainy):
    ''' Get a NB fit on the data '''
    # This can be updated later to use partial_fit to do big data learning
    gnb = GaussianNB()
    model = gnb.fit(trainx, trainy)
    return model

# Simply makes predictions on the testdata
# Returns a vector of predictions
def nb_predict(model, testx):
    ''' Make predictions using NB ''' 
    return model.predict(testx)

###############################################################################
# MISC FUNCTIONS
###############################################################################

def validate_algo(algostr):
    ''' Checks whether a string specifies a valid learning algorithm '''
    valids = {'nb'}

    if algostr in valids:
        return True
    return False
