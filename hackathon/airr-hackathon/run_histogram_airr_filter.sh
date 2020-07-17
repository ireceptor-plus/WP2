#!/bin/bash

if [ $# -ne 4 ];
then
    echo "Usage: $0 repertoireID fieldName filter baseURL"
    exit 1
fi

repertoire_id=$1
field_name=$2
filter_term=$3
url=$4

SCRIPT_DIR=`dirname "$0"`

filename=/tmp/ipa1_sample$sample.tsv
filename2=/tmp/ipa1_2_sample$sample.tsv

query=

# Get the data from the repository at the URL provided.
curl --insecure --data "{\"filters\": {\"op\":\"=\",\"content\": {\"field\":\"repertoire_id\",\"value\":\"$repertoire_id\"}},\"format\":\"tsv\"}" $url/airr/v1/rearrangement > $filename

egrep "$filter_term|$field_name" $filename > $filename2

# Finally we generate a heatmap given all of the processed information.
python3 $SCRIPT_DIR/airr_histogram.py $field_name $filename2 $field_name-$repertoire_id-$filter_term.png

# Clean up our temporary files.
#rm $filename
