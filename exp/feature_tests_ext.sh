#!/bin/bash

# feature_tests_ext.sh
# Zane Markel
# 8 JAN 2014
# This file runs an entropy-based decision tree trial on all databases in a directory
# The intention is to get decision tree graphs of isolated features in order to
# determine the information gain of that feature.
# This script extends the original feature_tests.sh by:
# 1. Testing on more samples with a range of malprev combinations
# 2. Using random forests
# 3. Aesthetically improving the names of the outputted files

# usage: ./feature_tests.sh DIRECTORY TRIAL.PY RESULTS_DIR SUMMARY_FILE GRAPHS_DIR

# -h option
if [ $1 = "-h" ]
then
    echo "usage: ./feature_tests.sh DIRECTORY TRIAL.PY RESULTS_DIR SUMMARY_FILE"
    exit
fi

dir=$1
trial=$2
resdir=$3
sumfi=$4

samples=35000
alg='rfc'
malfracs=('0.001' '0.01' '0.1' '0.25' '0.5' '0.75' '0.9')
seeds=('313379001')

echo "accuracy,precision,recall,f1,algorithm,malfrac_tr,malfrac_te,seed,feature" > $sumfi
for file in $dir*
do
    for tr in ${malfracs[@]}
    do
        for te in ${malfracs[@]}
        do
            for seed in ${seeds[@]}
            do
                bname=$(basename -s .csv $file)
                name="res-"$bname"-"$tr"-"$te"-"$seed
                echo $name 
                
                # Actually run a trial
                python $trial -s $seed -n $samples -m $tr $te $db $alg > $resdir$name

                # Add the results to the summary file
                python summarize.py -c "$alg,$tr,$te,$seed,$bname" $resdir$name >> $sumfi
            done
        done
    done
done
