#!/bin/bash

# heatmap.sh
# Zane Markel
# 8 JAN 2015
# A generalization of the ensemble script, which runs the same test for a given
# learning algorithm
# NOTE: There will be no graphs produced with these tests.

# usage: ./heatmap.sh DB TRIAL.PY RESULTS_DIR SUMMARY_FILE 

# -h option
if [ $1 = "-h" ]
then
    echo "usage: ${0} DB TRIAL.PY RESULTS_DIR SUMMARY_FILE ALGORITHM"
    exit
fi

db=$1
trial=$2
resdir=$3
sumfi=$4
alg=$5

samples=35000 # Keep the number of samples constant
malfracs=('0.001' '0.01' '0.1' '0.25' '0.5' '0.75' '0.9')
seeds=('313379001')

echo "accuracy,precision,recall,f1,algorithm,malfrac_tr,malfrac_te,seed" > $sumfi
for tr in ${malfracs[@]}
do
    for te in ${malfracs[@]}
    do
        for seed in ${seeds[@]}
        do
            name="res-"$alg"-"$tr"-"$te"-"$seed
            echo $name 
            
            # Actually run a trial
            python $trial -s $seed -n $samples -m $tr $te $db $alg > $resdir$name

            # Add the results to the summary file
            python summarize.py -c "$alg,$tr,$te,$seed" $resdir$name >> $sumfi
        done
    done
done
