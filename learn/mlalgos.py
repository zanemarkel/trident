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
from sklearn.linear_model import LogisticRegression
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
    if(algoname == 'dte'):
        return tree.DecisionTreeClassifier(random_state = seed, \
                criterion="entropy")
    if(algoname == 'lr'):
        return LogisticRegression(penalty='l1', class_weight='auto', random_state=seed)

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
    if(algoname == 'dte'):
        return dte_fit(trainx, trainy, seed)

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
# LOGISTIC REGRESSION
###############################################################################

# LR fit on data
# Returns a LogisticRegression.fit object
def lr_fit(trainx, trainy, seed=0):
    ''' Get a LR fit on the data '''
    # This can be updated later to use partial_fit to do big data learning
    lr_est = LogisticRegression(penalty='l1', class_weight='auto', random_state=seed)
    model = lr_est.fit(trainx, trainy)
    return model

# Simply makes predictions on the testdata
# Returns a vector of predictions
def lr_predict(model, testx):
    ''' Make predictions using LR ''' 
    return model.predict(testx)

def lr_crossv_getC(trainx, trainy, Carr=[0.1, 1.0, 10.0, 100.0], seed=0):
    ''' Get an appropriate C value for the LR. 
    Carr is the array of C values to test. '''
    
    # Get stratified k folds
    skf = cross_validation.StratifiedKFold(trainy, n_folds=10)

    # Cross-validate for the best C
    best_c = 0
    best_score = 0
    for this_c in Carr:
        lr_est = LogisticRegression(penalty='l1', class_weight='auto', C=this_c, random_state=seed)
        scores = cross_validation.cross_val_score(lr_est, trainx, y=trainy, \
                    scoring='f1', cv=skf)
        # If this this_c scored, on average, better than the best C value so far, update best_c
        this_score = scores.mean()
        print 'This score and C: ', this_score, this_c
        if this_score > best_score:
            best_score = this_score
            best_c = this_c

    return best_c


###############################################################################
# DECISION TREE
###############################################################################

def dt_graph(treeest, cv, scores, features, labels, featnames, outfile):
    ''' Retrains the tree estimator using the fold with the best results
    from the cross-validation process. Prints out a graph pdf file of 
    that estimator.'''
    # Hacky way to get the training data for the best fold
    bestfold = np.argmax(scores)
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

def dte_fit(trainx, trainy, seed):
    ''' Get a decision tree (CART) fit on the data 
    Uses information gain instead of gini'''
    cdt = tree.DecisionTreeClassifier(random_state = seed, criterion='entropy')
    model = cdt.fit(trainx, trainy)
    return model

def dte_predict(model, testx):
    ''' Make predictions using a CART decision tree.
    Uses information gain instead of gini'''
    return model.predict(testx)

def dt_predict(model, testx):
    ''' Make predictions using a CART decision tree. '''
    return model.predict(testx)

###############################################################################
# MISC FUNCTIONS
###############################################################################

def validate_algo(algostr):
    ''' Checks whether a string specifies a valid learning algorithm '''
    valids = {'nb', 'dt', 'dte', 'lr'}

    if algostr in valids:
        return True
    return False
