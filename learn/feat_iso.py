''' This script will assist with feature isolation by making new databases with
just the isolated feature, the filename, and the label.'''
# Author: Zane Markel
# Created: 16 SEP 2014

import mldata
import numpy as np
import argparse

clargs = argparse.ArgumentParser()
clargs.add_argument('db', type=file, \
    help='The database file that you want to split by feature.')
clargs.add_argument('outdir', help='directory to output to.')
args = clargs.parse_args()
db = args.db
outdir = args.outdir

# Load the data
data = mldata.load_data(db)

# Get the feature names
_, _, _, featurenames = mldata.data_components(data)

# For each feature, save a new database with it, the label, and the fname
nonfeats = ['isMalware', 'Name']
for feat in featurenames:
    thisdata = mldata.only_features(data, nonfeats+[feat])
    fname = '{}{}.csv'.format(outdir, feat)
    print fname
    mldata.save_data(thisdata, open(fname, 'w'))
