""" Run a single machine learning trial. """
###############################################################
# Author:       Zane Markel
# Created:      20 FEB 2013
#
# Name:         trial
# Description:  Controls a single machine learning trial.
#               Basically, this program puts together all the 
#               other programs needed to run a trial.
#               Works independently, or oldtrial can be called
#               from another script
###############################################################

import mldata
import mlalgos
import mlstat
import sys
import optparse
import argparse
from pprint import pprint
from sklearn import cross_validation
from sklearn import tree
from sklearn.metrics import fbeta_score, make_scorer
#import pydot
#from sklearn.externals.six import StringIO

def main():

    # Parse the command line options
    options = clargs()

    # Actually run the trial
    sometrials(options)


def sometrials(options):
    ''' Runs a single machine learning trial. '''
    
    # Load the data
    data = mldata.load_data(options.database)

    # Preprocess data
    # TODO: fill in this part

    # If specified, output the current database
    if(options.exportdb != None):
        mldata.save_data(data, options.exportdb)

    # Extract the basic data from the data
    features, labels, _, featnames = mldata.data_components(data)

    # Get the seeds for the splits.
    numsplits = 30 # Make this an option later, if need be.
    seeds = mldata.gen_seeds(options.seed, numsplits)

    # Generate the splits
    # For now, training data will compose 90% of each split.
    # Possibly make the an option later.
    tr_te_sizes = [int(round(0.9*options.numsamples)), \
        options.numsamples-int(round(0.9*options.numsamples))]
    splits = mldata.gen_splits(seeds, labels, tr_te_sizes, options.malfrac) 

    # Start printing the results
    printparams(options)
    mlstat.print_results_header()

    # make the fbeta scoring object
    scorer = make_scorer(fbeta_score, beta=options.beta)

    # Fit and score based on the various performance measures
    perfmeasures = ['accuracy', 'precision', 'recall', scorer]
    for perfmeasure in perfmeasures:
        score_on_splits(perfmeasure, options, features, labels, featnames, splits)

    return

def score_on_splits(perfmeasure, options, features, labels, featnames, splits):
    ''' Actually do the fitting and evaluating.

    perfmeasure = scoring mechanic. e.g. 'accuracy', 'precision', 'recall', 'f1'
        (this can be a scoring object or a string)
    options = the command line arguments
    features = the data records
    labels = the data labels
    featnames = names of the features of each record. From mldata.data_component
    splits = the results of, say, mldata.gen_splits

    returns (average of scores, standard deviation of scores, and the scores)
    '''

    # Score the splits
    est = mlalgos.get_estimator(options.algorithm, seed=options.seed)
    scores = cross_validation.cross_val_score(est, features, y=labels, \
                scoring=perfmeasure, cv=splits)

    # Print the results
    metric = 'ERROR'
    if(isinstance(perfmeasure, basestring)):
        metric = perfmeasure
    else:
        metric = 'f-'+str(options.beta)
    mlstat.printresults(metric, scores)

    # Icing on the cake: draw a decision tree graph
    # based on the fold with the best f1 score
    if(perfmeasure=='f1' and options.graphfile != None and \
        isinstance(est, tree.DecisionTreeClassifier)):
        mlalgos.dt_graph(est, splits, scores, features, labels, \
                        featnames, options.graphfile)

    return (scores.mean(), scores.std(), scores)


def oldtrial(options):
    ''' Run a single machine learning trial.''' 
    # TODO: make option for loading intermediate data to skip steps that have
    # been done in previous trials

    # Select data to read
    data = mldata.load_data(options.database)

    # Get a sample
    if(options.numsamples != None): # Check to see if a sample was requested
        if(options.malfrac != None):
            sample = mldata.select_sample(int(options.seed), data, \
                options.numsamples, options.malfrac[0])
        else: # Only use a percent malware if one was specified
            sample = mldata.select_sample(int(options.seed), data,
                options.numsamples)
    else:
        sample = data

    # If specified, output the current database
    if(options.exportdb != None):
        mldata.save_data(sample, options.exportdb)

    # Original way to run a trial... probably going to be deleted eventually
    if(options.acc):
        return oldacc(options, sample)

    # Primary way to run a trial
    else:
        printparams(options)
        mlstat.print_results_header()
        perfmeasures = ['accuracy', 'precision', 'recall', 'f1']
        avgs = []
        for perfmeasure in perfmeasures:
            # Extract the parts of the samples
            # Not yet using the filenames and feature names
            features, labels, _, featnames = mldata.data_components(sample)

            # Split the sample into 10 randomly stratified folds
            cvsplits = cross_validation.StratifiedShuffleSplit(labels, \
                        test_size=0.1, random_state=options.seed)

            # Score the folds
            est = mlalgos.get_estimator(options.algorithm)
            scores = cross_validation.cross_val_score(est, features, y=labels, \
                        scoring=perfmeasure, cv=cvsplits)

            # Print the results
            avgs.append(sum(scores)/len(scores))
            avgstr = '{:.4}'.format(avgs[-1]).rjust(7)
            resultstr = '{}  {} '.format(perfmeasure.rjust(9), avgstr)
            for score in scores:
                resultstr += ' {:.3}'.format(score)
            print(resultstr)

            # Icing on the cake: draw a decision tree graph
            # based on the fold with the best f1 score
            if(perfmeasure=='f1' and options.graphfile != None and \
                isinstance(est, tree.DecisionTreeClassifier)):
                mlalgos.dt_graph(est, cvsplits, scores, features, labels, \
                                featnames, options.graphfile)

        return (perfmeasures, avgs)

def printparams(options):
    ''' Print the command line options for later reference '''
    print('{}'.format(str(options).strip('[]') ) )

def clargs():
    ''' Takes care of parsing the command line options. '''

    parser = argparse.ArgumentParser(
        description='Run a single machine learning trial')
    parser.add_argument('database', type=argparse.FileType('r'), \
        help='The csv database file to use')
    parser.add_argument('algorithm', \
            choices=['nb', 'dt', 'dte', 'lr', 'rfc', 'abc', 'bac', 'svm'], \
            help='The learning argument to use.')
    parser.add_argument('-s', '--seed', type=int, required=True, \
        help='integer seed to use (for repeating random trials)')
    parser.add_argument('-n', '--numsamples', type=int, \
        help='integer number of samples to use from the database.')
    parser.add_argument('-m', '--malfrac', nargs=2, type=float, \
        metavar=('TRNG', 'TEST'), \
        help='fraction (as a decimal) of samples that will be malicious. \
        TRNG is the fraction for the training data. \
        TEST is the fraction for the test data.')
    parser.add_argument('-e', '--exportdb', type=argparse.FileType('w'), \
        help='file to export post-sampled/preprocessed database to')
    parser.add_argument('--acc', default=False, action='store_true', \
        help='Run a simple accuracy trial without CV')
    parser.add_argument('-b', '--beta', default=1.0, type=float, \
        help='specify a beta for the fbeta score.')
    # The graphfile is taken as a string because that's how the library takes it
    parser.add_argument('-g', '--graphfile', \
        help='if decision trees are used, specifies a file to write a graph to')
    args = parser.parse_args()

    return args

def oldacc(options, sample):
    ''' The simpleAcc way of running a trial ''' 
    # Get the final components from the data
    print("Building train and test data...")

    # Just partition it 80-20 training-testing
    trainsize = 0.8 * len(sample)
    train = sample[0:trainsize]
    test = sample[trainsize:]
    trfeat, trlab, _, _ = mldata.data_components(train)
    tefeat, telab, _, _ = mldata.data_components(test)

    # Check for valid learning algorithm
    if(not mlalgos.validate_algo(options.algorithm)):
        print("Invalid learning algorithm %s" % (options.algorithm))
        sys.exit(1)

    # Train
    print("Training...")
    model = mlalgos.learn(options.algorithm, trfeat, trlab, options.seed)

    # Test
    print("Testing...")
    preds = mlalgos.predict(model, tefeat)

    # Analyze -- FScore, acc, learning curves
    print("Results:")
    printparams(options) # CL options

    # Model parameters
    pprint(vars(model))

    accuracy = mlstat.acc(preds, telab)
    print("Accuracy: %f" % (accuracy))

    return (['accuracy'], [accuracy])

if __name__ == '__main__':
    main()
