#!/bin/bash

# ensemble.sh
# Zane Markel
# 10 NOV 2014
# This trial will run trials of decision trees, AdaBoost, Random Forests, and
# Bagging on a variety of malprev combinations
# NOTE: There will be no graphs produced with these tests.

# usage: ./ensemble.sh DB TRIAL.PY RESULTS_DIR SUMMARY_FILE 

# -h option
if [ $1 = "-h" ]
then
    echo "usage: ${0} DB TRIAL.PY RESULTS_DIR SUMMARY_FILE GRAPHS_DIR"
    exit
fi

db=$1
trial=$2
resdir=$3
sumfi=$4

samples=2500 # Keep the number of samples constant
algs=('dte' 'rfc' 'abc' 'bac')
malfracs=('0.001' '0.01' '0.1' '0.25' '0.5' '0.75' '0.9')
seeds=('313379001')

echo "accuracy,precision,recall,f1,algorithm,malfrac_tr,malfrac_te,seed" > $sumfi
for i in ${algs[@]}
do
    for tr in ${malfracs[@]}
    do
        for te in ${malfracs[@]}
        do
            for seed in ${seeds[@]}
            do
                name="res-"$i"-"$tr"-"$te"-"$seed
                echo $name 
                
                # Actually run a trial
                python $trial -s $seed -n $samples -m $tr $te $db $i > $resdir$name

                # Add the results to the summary file
                python summarize.py -c "$i,$tr,$te,$seed" $resdir$name >> $sumfi
            done
        done
    done
done
