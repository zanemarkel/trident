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

def main():
    ''' Run a single machine learning trial. ''' 
    # parse cmd line args
    # TODO: make option for loading intermediate data to skip steps that have
    # been done in previous trials

    # When cmd line args are lacking...
    csv = raw_input("Which file should be used? ")
    algo = raw_input("Which learning algorithm? (nb)")
    seed = raw_input("Seed? (must be an int) ")

    # Select data to read
    print("Loading data...")
    data = mldata.load_data(csv)

    # Get a sample
    # Just using 100 malicious files and 900 benign files for now
    print("Getting sample...")
    samplesize = 1000
    fracmal = 0.1
    sample = mldata.select_sample(int(seed), data, samplesize, fracmal)

    # Preprocess data
    # TODO: fill in this part

    # Get the final components from the data
    print("Building train and test data...")
    trainsize = 0.8 * len(sample)
    train = sample[0:trainsize]
    test = sample[trainsize:]
    trfeat, trlab, trnmes, featnames = mldata.data_components(train)
    tefeat, telab, tenmes, _ = mldata.data_components(test)

    # OLD STUFF:
    #features, labels, recnames, featnames = mldata.data_components(data)
    #trainx = features
    #trainy = labels
    #testx = features

    # Check for valid learning algorithm
    if(not mlalgos.validate_algo(algo)):
        print("Invalid learning algorithm %s" % (algo))
        sys.exit(1)

    # Train
    print("Training...")
    model = mlalgos.learn(algo, trfeat, trlab)

    # Test
    print("Testing...")
    preds = mlalgos.predict(model, tefeat)

    # Analyze -- FScore, acc, learning curves
    print("Results:")
    accuracy = mlstat.acc(preds, telab)
    print("Accuracy: %f" % (accuracy))
    

if __name__ == '__main__':
    main()
