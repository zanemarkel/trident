#!/bin/bash

# Zane Markel
# 21 JAN 2015
# sums_a_dir.sh

# this is just a simple script that looks at all the results files in a given
# directory and writes a (new version) summary file of them to stdout.
# Usage: ./sums_a_dir.sh [dir]
# NOTE: it is assumed that results files start with res

# Write the header line
python newsums.py

for resfile in $(ls $1 | grep ^res)
do
    python newsums.py $1'/'$resfile
done
