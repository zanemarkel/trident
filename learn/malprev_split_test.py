''' Test malprev by splitting data into databases with different malware
prevalences. '''
################################################################################
# Author: Zane Markel
# Created 16 SEP 2014
#
# malprev_split_test.py
################################################################################

import numpy as np
import argparse
import mldata

def main():
    ''' Test the functionality of splitting malprevs by taking a database and
    splitting into the splits. '''

    clparse = argparse.ArgumentParser('Test malprev splitting functionality.')
    clparse.add_argument("db", type=file, \
        help='.csv containing the database to test with')
    clparse.add_argument("outdir", help='directory to output to.')
    args = clparse.parse_args()

    data = mldata.load_data(args.db)
    feat, lab, _, _ = mldata.data_components(data)

    seeds = mldata.gen_seeds(42, 3)

    # Split the data twice. This is a proof of concept, so don't
    # worry that you're hardcoding the numsamples and the malprevs
    splits = mldata.gen_splits(seeds, lab, [9000,1000], [0.5, 0.1])

    # This parallels how the iteration works in cross_validation.cross_val_score
    cnt = 0
    for tr_idx, te_idx in splits:
        # Training data
        handle_idx(tr_idx, data, args, 'tr{}'.format(cnt))
        # Test data
        handle_idx(te_idx, data, args, 'te{}'.format(cnt))
        cnt += 1

def handle_idx(idx, data, args, name):
    '''Computes and prints the malprev, then saves the data where specified '''
    print('{} of {} are malicious'.format( \
        sum(data[idx]['isMalware']), len(data[idx])))
    outname = args.outdir + '{}'.format(name) # name the file
    mldata.save_data(data[idx], open(outname, 'w')) # save the appropriate data

if __name__ == '__main__':
    main()
