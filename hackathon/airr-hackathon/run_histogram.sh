#!/bin/bash

if [ $# -ne 3 ];
then
    echo "Usage: $0 sampleID fieldName baseURL"
    exit 1
fi

sample=$1
field_name=$2
url=$3

SCRIPT_DIR=`dirname "$0"`

filename=/tmp/ipa1_sample$sample.tsv

# Get the data from the repository at the URL provided.
curl -k -X POST  -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "ir_project_sample_id_list[]=$sample" -d "output=tsv" -d "ir_data_format=airr" $url/v2/sequences_data > $filename

# Finally we generate a heatmap given all of the processed information.
python3 $SCRIPT_DIR/airr_histogram.py $field_name $filename $field_name-sample$sample.png

# Clean up our temporary files.
#rm $filename
