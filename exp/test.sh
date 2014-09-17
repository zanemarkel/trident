#!/bin/bash

malfracs=('0.5' '0.1' '0.01' '0.001')

for j in ${malfracs[@]}
do
    if [ "$j" != "0.5" ]
    then
        echo "$j is not 0.5!"
    fi
done
