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
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn import cross_validation
import pydot
from sklearn.externals.six import StringIO



###############################################################################
# WRAPPER FUNCTIONS
###############################################################################

def get_estimator(algoname, seed=0):
    ''' Returns an estimator object based on the string algoname
    Valid options are outlined in validate_algos().
    Estimators that require a random seed (e.g. dt), should be passed
    a non-zero seed'''

    if(algoname == 'nb'):
        return GaussianNB()

    if(algoname == 'dt'):
        return tree.DecisionTreeClassifier(random_state = seed)

    # You only get here if the string was invalid
    print("Unrecognized algorithm name")
    return

# This function will be used to learn using an arbitrary algorithm
def learn(algoname, trainx, trainy, seed):
    '''
Learn using an arbitrary algorithm. The choices for algoname are:
nb = Naive Bayes
dt = Decision Tree (CART)
'''
    if(algoname == 'nb'):
        return nb_fit(trainx, trainy)

    if(algoname == 'dt'):
        return dt_fit(trainx, trainy, seed)

    # You only get here if the string was invalid
    print("Unrecognized algorithm name")
    return

# Make predictions using a model
def predict(model, testx):
    ''' Make predictions using a model generated from the learn function.'''
    if( isinstance(model, GaussianNB)):
        return nb_predict(model, testx) 
    elif( isinstance(model, tree.DecisionTreeClassifier)):
        return dt_predict(model, testx)
    else:
        print("Unrecognized model")
        return

# Get the parameters from a model
def params(model):
    ''' Get the parameters in a model '''
    if( isinstance(model, GaussianNB)):
        return model.get_params() 
    if( isinstance(model, tree.DecisionTreeClassifier)):
        return model.get_params() 

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
# DECISION TREE
###############################################################################

def dt_graph(treeest, cv, scores, features, labels, featnames, outfile):
    ''' Retrains the tree estimator using the fold with the best results
    from the cross-validation process. Prints out a graph pdf file of 
    that estimator.'''
    # Hacky way to get the training data for the best fold
    bestfold = np.argmax(scores)
    print(bestfold)
    cnt = 0
    for train, _ in cv:

        # Only do stuff when you've got the training indices for the best fold
        if(cnt == bestfold):
            # Fit
            treeest.fit(features[train], labels[train])

            # Get the dot file
            dot_data = StringIO()
            tree.export_graphviz(treeest, out_file=dot_data, \
                feature_names=featnames)

            # Convert the dot file to a graph
            graph = pydot.graph_from_dot_data(dot_data.getvalue())
            graph.write_pdf(outfile)
            return
        else:
            cnt += 1

    print("You should never see this text from dt_graph!")
    return

def dt_fit(trainx, trainy, seed):
    ''' Get a decision tree (CART) fit on the data '''
    cdt = tree.DecisionTreeClassifier(random_state = seed)
    model = cdt.fit(trainx, trainy)
    return model

def dt_predict(model, testx):
    ''' Make predictions using a CART decision tree. '''
    return model.predict(testx)

###############################################################################
# MISC FUNCTIONS
###############################################################################

def validate_algo(algostr):
    ''' Checks whether a string specifies a valid learning algorithm '''
    valids = {'nb', 'dt'}

    if algostr in valids:
        return True
    return False
