#!/bin/bash

# $1 refers to the python file executed. In our case it is either create_baseline_features.py or create_advanced_features.py
# $2 refers to the path containing all the csv files which can either be the path to the training data or the test data.
# $3 refers to the output file which contains the output from STDOUT. 

for filename in $2/*.csv; do
    python3 $1 $filename >> $3
done
