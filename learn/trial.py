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
import sys

def main():
    ''' Run a single machine learning trial. ''' 
    # parse cmd line args
    # TODO: make option for loading intermediate data to skip steps that have
    # been done in previous trials

    # When cmd line args are lacking...
    matfile = raw_input("Which matrix file should be used? ")
    algo = raw_input("Which learning algorithm? (nb)")

    # Select data to read
    features, labels = mldata.load_data(matfile)

    # Preprocess data

    # For now just use the data as both the training data and the test data
    trainx = features
    trainy = labels
    testx = features

    # Check for appropriate learning algorithm
    if(not mlalgos.validate_algo(algo)):
        print("Invalid learning algorithm %s" % (algo))
        sys.exit(1)

    # Train
    model = mlalgos.learn(algo, trainx, trainy)

    # Test
    preds = mlalgos.predict(model, testx)

    # Analyze -- FScore, acc, learning curves
    

if __name__ == '__main__':
    main()
