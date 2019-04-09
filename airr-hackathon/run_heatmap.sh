#!/bin/bash

sample=$1
url=https://ipa1.ireceptor.org

filename=/tmp/ipa1_sample$sample.tsv
filename2=/tmp/ipa1_filter_sample$sample.tsv
x_column=v_call
y_column=j_call

curl -k -X POST -d "ir_project_sample_id_list[]=$sample" -d "output=tsv" -d "ir_data_format=airr" $url/v2/sequences_data > $filename
cat $filename | awk 'BEGIN {FS="\t"; print("v_call\tj_call")} /IG/ {printf("%s\t%s\n",substr($7,0,index($7,"*")-1), substr($8,0,index($8,"*")-1))}' > $filename2
xvals=`cat $filename2 | cut -f 1 | awk 'BEGIN {FS=","} /IG/ {print($1)} /TR/ {print($1)}' | sort | uniq | awk '{if (NR>1) printf(",%s", $1); else printf("%s", $1)}'`
echo "$xvals"
yvals=`cat $filename2 | cut -f 2 | awk 'BEGIN {FS=","} /IG/ {print($1)} /TR/ {print($1)}' | sort | uniq | awk '{if (NR>1) printf(",%s", $1); else printf("%s", $1)}'`
echo "$yvals"
python airr_heatmap.py v_call j_call $xvals $yvals $filename2 $x_column-$y_column-sample$sample.png

rm $filename
rm $filename2
