#!/bin/bash
curl -s -S -k -X POST  -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" $1/v2/samples

