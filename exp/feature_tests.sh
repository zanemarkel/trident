#!/bin/bash

# feature_tests.sh
# Zane Markel
# 18 SEP 2014
# This file runs an entropy-based decision tree trial on all databases in a directory
# The intention is to get decision tree graphs of isolated features in order to
# determine the information gain of that feature.

# usage: ./feature_tests.sh DIRECTORY TRIAL.PY RESULTS_DIR SUMMARY_FILE GRAPHS_DIR

# -h option
if [ $1 = "-h" ]
then
    echo "usage: ./feature_tests.sh DIRECTORY TRIAL.PY RESULTS_DIR SUMMARY_FILE GRAPHS_DIR"
    exit
fi

dir=$1
trial=$2
resdir=$3
sumfi=$4
gradir=$5

samples=10000
alg='dte'
malfracs='0.5 0.5'
seed='1029384756'

echo "accuracy,precision,recall,f1,algorithm,malfrac_tr,malfrac_te,seed,feature" > $sumfi
for file in $dir*
do
    bname=$(basename $file)
    name=$bname"-test"
    graphstr="-g "$gradir$name"-graph.pdf"
    echo $name
    python $trial -s $seed -n $samples -m $malfracs $graphstr $file $alg > $resdir$name
    python summarize.py -c "$alg,$malfracs,$seed,$bname" $resdir$name >> $sumfi
done
