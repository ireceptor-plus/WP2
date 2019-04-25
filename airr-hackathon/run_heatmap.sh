#!/bin/bash

if [ $# -ne 2 ];
then
    echo "Usage: $0 sampleID BaseURL"
    exit 1
fi

sample=$1
url=$2

filename=/tmp/ipa1_sample$sample.tsv
filename2=/tmp/ipa1_filter_sample$sample.tsv
x_column_str=v_call
y_column_str=j_call

SCRIPT_DIR=`dirname "$0"`

# Get the data from the repository at the URL provided.
curl -k -X POST  -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "ir_project_sample_id_list[]=$sample" -d "output=tsv" -d "ir_data_format=airr" $url/v2/sequences_data > $filename

# Get the columns numbers for the column labels of interest.
x_column=`cat $filename | awk -F"\t" -v label=$x_column_str '{for(i=1;i<=NF;i++){if ($i == label){print i}}}'` 
y_column=`cat $filename | awk -F"\t" -v label=$y_column_str '{for(i=1;i<=NF;i++){if ($i == label){print i}}}'` 
#echo $x_column
#echo $y_column

# Extract the two columns of interest. In this case we want the gene (not including the allele)
# As a result we chop things off at the first star. This also takes care of the case where
# a gened call has multiple calls. Since we drop everthing after the first allele we drop all of 
# the other calls as well.
cat $filename | cut -f $x_column,$y_column | awk -v xlabel=$x_column_str -v ylabel=$y_column_str 'BEGIN {FS="\t"; printf("%s\t%s\n", xlabel, ylabel)} /IG|TR/ {printf("%s\t%s\n",substr($1,0,index($1,"*")-1), substr($2,0,index($2,"*")-1))}' > $filename2

# Generate a set of unique values that we can generate the heatmap on. This is a comma separated
# list of unique gene names for each of the two fields of interest.
xvals=`cat $filename2 | cut -f 1 | awk 'BEGIN {FS=","} /IG/ {print($1)} /TR/ {print($1)}' | sort | uniq | awk '{if (NR>1) printf(",%s", $1); else printf("%s", $1)}'`
yvals=`cat $filename2 | cut -f 2 | awk 'BEGIN {FS=","} /IG/ {print($1)} /TR/ {print($1)}' | sort | uniq | awk '{if (NR>1) printf(",%s", $1); else printf("%s", $1)}'`

# Finally we generate a heatmap given all of the processed information.
echo "$x_column_str"
echo "$y_column_str"
echo "$xvals"
echo "$yvals"
python3 $SCRIPT_DIR/airr_heatmap.py $x_column_str $y_column_str $xvals $yvals $filename2 $x_column_str-$y_column_str-sample$sample.png

# Clean up our temporary files.
#rm $filename
#rm $filename2
