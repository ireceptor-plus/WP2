#!/bin/bash

# Get the location of the directory where the script was run.
PROG_NAME=`basename "$0"`
SCRIPT_DIR=`dirname "$0"`
PYTHON_PROG="test_airr_api.py"

# Environment checks
#echo $PROG_NAME
#echo $SCRIPT_DIR
#python --version


NB_ARGS=3
if [ $# -lt $NB_ARGS ];
then
    echo "$PROG_NAME: wrong number of arguments ($# instead of at least $NB_ARGS)"
    echo "usage: $PROG_NAME adc_url entry_point <json_query> [<json_query> ...]"
    exit 1
fi

# Get the URL and shift the parameters.
adc_url="$1"
shift
# Get the API entry point and shift the parameters.
entry_point="$1"
shift

# For the remainder of command line parameters, treat each as a JSON query.
let "error_count=0"
let "total_count=0"
while [ "$1" != "" ]; do
    filename="$1"
    # Run the python code (python 3 required) to test the API query
    python3 $SCRIPT_DIR/$PYTHON_PROG $adc_url $entry_point $filename
    error_code=$?
    if [ $error_code -ne 0 ]
    then
        let "error_count=error_count+1"
    fi
    # Process the next command line arguement.
    shift
    let "total_count=total_count+1"
done

if [ $error_count -gt 0 ]
then
    echo "SUMMARY: $error_count of $total_count tests failed"
else
    echo "SUMMARY: All tests passed!!!"
fi
