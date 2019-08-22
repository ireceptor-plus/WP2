#!/bin/bash

# Get the location of the directory where the script was run.
SCRIPT_DIR=`dirname "$0"`

NB_ARGS=3
if [ $# -lt $NB_ARGS ];
then
    echo "$0: wrong number of arguments ($# instead of at least $NB_ARGS)"
    echo "usage: $0 adc_url entry_point <json_query> [<json_query> ...]"
    exit 1
fi

# Get the URL and shift the parameters.
adc_url="$1"
shift
# Get the API entry point and shift the parameters.
entry_point="$1"
shift

# For the remainder of command line parameters, treat each as a JSON query.
while [ "$1" != "" ]; do
    filename="$1"
    # Do the CURL command and report if the command exits properly
    # The --fail tells curl to fail with error 22 on an HTTP error.
    echo "curl -s --data @$filename https://$adc_url/$entry_point"
    curl -s --fail --data @$filename https://$adc_url/$entry_point 
    error_code=$?
    if [ $error_code -ne 0 ]
    then
        echo "ERROR: Query $filename to $adc_url/$entry_point failed with exit code: $?"
    else
        echo "Query $filename to $adc_url/$entry_point passed!"
    fi
    # Process the next command line arguement.
    shift
done

