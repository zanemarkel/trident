#!/bin/bash

# spring14runs.sh
# Zane Markel
# 6 APR 2014
# This file will run all the trials necessary for the spring 2014 paper

# usage: ./spring14runs.sh DB TRIAL.PY RESULTS_DIR SUMMARY_FILE GRAPHS_DIR

# -h option
if [ $1 = "-h" ]
then
    echo "usage: ./spring14runs.sh DB TRIAL.PY RESULTS_DIR SUMMARY_FILE GRAPHS_DIR"
    exit
fi

db=$1
trial=$2
resdir=$3
sumfi=$4
gradir=$5

# just a test
#echo $db' '$resdir' '$sumfi

samples=50000 # Keep the number of samples constant
algs=('nb' 'dt' 'dte')
malfracs=('0.5' '0.2' '0.1' '0.01' '0.001')
seeds=('3574682466873' '1946873456497' '32546815137583')

echo "accuracy,precision,recall,f1,algorithm,malfrac,seed" > $sumfi
for i in ${algs[@]}
do
    for j in ${malfracs[@]}
    do
        for k in ${seeds[@]}
        do
            name="res-"$i"-"$j"-"$k
            echo $name 
            
            # Var to print a graph for decision trees
            g=""
            if [[ $i = "dt" || $i = "dte" ]]
            then
                g="-g "$gradir$name"-graph.pdf"
            fi

            python $trial -d $db -s $k -n $samples -m $j -a $i $g > $resdir$name
            python summarize.py -c "$k" $resdir$name >> $sumfi
        done
    done
done
