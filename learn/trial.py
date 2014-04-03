""" Run a single machine learning trial. """
###############################################################
# Author:       Zane Markel
# Created:      20 FEB 2013
#
# Name:         trial
# Description:  Controls a single machine learning trial.
#               Basically, this program puts together all the 
#               other programs needed to run a trial.
#
#               
#               
#               
#               
#               
###############################################################

import mldata
import mlalgos
import mlstat
import sys
import optparse
from pprint import pprint
from sklearn import cross_validation
from sklearn import tree
import pydot
from sklearn.externals.six import StringIO

def main():
    ''' Run a single machine learning trial. ''' 
    # TODO: make option for loading intermediate data to skip steps that have
    # been done in previous trials

    # Parse the command line options
    options = clargs()

    # Select data to read
    print("Loading data...")
    data = mldata.load_data(options.database)

    # Get a sample
    if(options.numsamples != None): # Check to see if a sample was requested
        print("Getting sample...")
        if(options.malfrac != None): 
            sample = mldata.select_sample(int(options.seed), data, \
                options.numsamples, options.malfrac)
        else: # Only use a percent malware if one was specified
            sample = mldata.select_sample(int(options.seed), data,
                options.numsamples)
    else:
        sample = data

    # Preprocess data
    # TODO: fill in this part

    # If specified, output the current database
    if(options.newdb != None):
        mldata.save_data(sample, options.newdb)

    # Original way to run a trial... probably going to be deleted eventually
    if(options.simplyAcc):
        oldacc(options, sample)

    # Primary way to run a trial
    else:
        print
        printparams(options)
        print('  Measure  Average  Fold-Scores')
        perfmeasures = ['accuracy', 'precision', 'recall', 'f1']
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
            avgstr = '{:.4}'.format(sum(scores)/len(scores)).rjust(7)
            resultstr = '{}  {} '.format(perfmeasure.rjust(9), avgstr)
            for score in scores:
                resultstr += ' {:.3}'.format(score)
            print(resultstr)

            # Icing on the cake: draw a decision tree graph
            # Using the tree from the last fold
            if(options.graphfile != None and \
                isinstance(est, tree.DecisionTreeClassifier)):
                printgraph(est, options.graphfile, featnames)

def printgraph(treeest, graphfile, featnames):
    ''' Prints a pdf with a graph of the decision tree '''
    dot_data = StringIO.StringIO()
    tree.export_graphviz(treeest, out_file=dot_data, feature_names = featnames)
    graph = pydot.graph_from_dot_data(dot_data.getvalue())
    graph.write_pdf(graphfile)

def printparams(options):
    ''' Print the command line options for later reference '''
    print('Results using: {}'.format(str(options).strip('[]') ) )

def clargs():
    ''' Takes care of parsing the command line options. '''
    # Handle options
    # TODO: switch to argparse
    parser = optparse.OptionParser("usage: %prog -d <directory>")
    parser.add_option('-d', '--database', dest='database', type='string', \
        help='The csv database file to use')
    parser.add_option('-a', '--algo', dest='algorithm', type='string', \
        help='The learning algorithm to use (nb, dt)')
    parser.add_option('-s', '--seed', dest='seed', type='int', \
        help='integer seed to use (for repeating random trials)')
    parser.add_option('-n', '--numsamples', dest='numsamples', type='int', \
        help='integer number of samples to use from the database \
        if unspecified, all samples will be used.')
    parser.add_option('-m', '--percentmalicious', dest='malfrac', type='float'\
        , help='fraction of samples that will be malicious \t\t\
        has no effect unless --numsamples is used')
    parser.add_option('-e', '--export', dest='newdb', type='string', \
        help='file to export post-sampled/preprocessed database to')
    parser.add_option('--acc', dest='simplyAcc', default=False, \
        action="store_true", help='Run a simple accuracy test instead of CV')
    parser.add_option('-g', '--graphfile', dest='graphfile', type='string', \
        help='if decision trees are used, specifies a file to write a graph to')
    (options, _) = parser.parse_args()
    if(options.database == None):
        options.database = raw_input("csv database file? ")
    if(options.algorithm == None):
        options.algorithm = raw_input("learning algorithm? (nb, dt) ")
    if(options.seed == None):
        options.seed = raw_input("seed? (must be an int) ")

    return options

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



if __name__ == '__main__':
    main()
