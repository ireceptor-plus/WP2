#!/bin/bash
if [ $# -ne 1 ];
then
    echo "Usage: $0 BaseURL"
    exit 1
fi

curl -s -S -k -X POST  -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" $1/v2/samples

