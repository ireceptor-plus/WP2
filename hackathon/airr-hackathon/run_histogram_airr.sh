#!/bin/bash

if [ $# -ne 3 ];
then
    echo "Usage: $0 repertoireID fieldName baseURL"
    exit 1
fi

repertoire_id=$1
field_name=$2
url=$3

SCRIPT_DIR=`dirname "$0"`

filename=/tmp/ipa1_sample$sample.tsv

# Get the data from the repository at the URL provided.
curl --insecure --data '{"filters": {"op":"=","content": {"field":"repertoire_id","value":"5efbc70e5f94cb6215deec8d"}},"format":"tsv"}' $url/airr/v1/rearrangement > $filename

# Finally we generate a heatmap given all of the processed information.
python3 $SCRIPT_DIR/airr_histogram.py $field_name $filename $field_name-sample$sample.png

# Clean up our temporary files.
#rm $filename
