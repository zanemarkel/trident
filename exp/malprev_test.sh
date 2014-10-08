#!/bin/bash

# malprev_test.sh
# Zane Markel
# 15 SEP 2014
# This file will run the trials to test varying malware prevalence between training and test data.

# usage: ./malprev_test.sh DB TRIAL.PY RESULTS_DIR SUMMARY_FILE GRAPHS_DIR

# -h option
if [ $1 = "-h" ]
then
    echo "usage: ./malprev_test.sh DB TRIAL.PY RESULTS_DIR SUMMARY_FILE GRAPHS_DIR"
    exit
fi

db=$1
trial=$2
resdir=$3
sumfi=$4
gradir=$5

# just a test
#echo $db' '$resdir' '$sumfi

samples=25000 # Keep the number of samples constant
algs=('nb' 'dt' 'lr')
malfracs=('0.5' '0.1' '0.01' '0.001')
seeds=('102938')

echo "accuracy,precision,recall,f1,algorithm,malfrac_tr,malfrac_te,seed" > $sumfi
for i in ${algs[@]}
do
    for j in ${malfracs[@]}
    do
        for k in ${seeds[@]}
        do
            name="res-"$i"-"$j"-"$j"-"$k
            echo $name 
            
            # Var to print a graph for decision trees
            g=""
            if [[ $i = "dt" || $i = "dte" ]]
            then
                g="-g "$gradir$name"-graph.pdf"
            fi

            # These lines run a trial with the same malfracs
            python $trial -s $k -n $samples -m $j $j $g $1 $i > $resdir$name
            python summarize.py -c "$i,$j,$j,$k" $resdir$name >> $sumfi

            # These lines run a trial with the training malfrac held at 0.5
            # Only do this if the malfrac is not already 0.5
            if [ "$j" != "0.5" ]
            then

                name="res-"$i"-0.5-"$j"-"$k
                echo $name 

                # Var to print a graph for decision trees
                g=""
                if [[ $i = "dt" || $i = "dte" ]]
                then
                    g="-g "$gradir$name"-graph.pdf"
                fi

                python $trial -s $k -n $samples -m 0.5 $j $g $1 $i > $resdir$name
                python summarize.py -c "$i,0.5,$j,$k" $resdir$name >> $sumfi
            fi
        done
    done
done
