# API hints and instructions

## Requirements

Requirements: python modules numpy, matplotlib, airr

## API Documentation

* [iReceptor Web Service API documentation](http://ireceptor.irmacs.sfu.ca/node/112)
* [AIRR Data Commons Web Service API documentation](https://github.com/airr-community/airr-standards/blob/metadata-docs/docs/api/overview.rst)

## Running the API based code

To run the generic histogram plot:

python graph_api.py v_call TRBV1,TRBV2,TRBV3,TRBV4,TRBV5,TRBV6,TRBV7 http://turnkey-test2.ireceptor.org

python graph_api.py v_call IGHV1,IGHV2,IGHV3,IGHV4,IGHV5,IGHV6,IGHV7 http://turnkey-test2.ireceptor.org

python graph_api.py junction_aa_length 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26 http://turnkey-test2.ireceptor.org

python graph_sample_api.py Patient3-T3 junction_aa_length 05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29 https://ipa4.ireceptor.org

python graph_sample_api.py p2255_d180_part1 v_call TRBV1,TRBV10,TRBV11,TRBV12,TRBV13,TRBV14,TRBV15,TRBV16,TRBV17,TRBV18,TRBV19,TRBV2,TRBV20,TRBV21,TRBV23,TRBV24,TRBV25,TRBV26,TRBV27,TRBV28,TRBV29,TRBV3,TRBV30,TRBV4,TRBV5,TRBV6,TRBV7,TRBV9 https://ipa3.ireceptor.org

python graph_sample_api.py Patient3-T1 v_call 'TRBV7-1,TRBV7-2,TRBV7-3,TRBV7-4,TRBV7-5,TRBV7-6,TRBV7-7,TRBV7-8,TRBV7-9,TRBV7-10,TRBV7-11,TRBV12-4*02' https://ipa4.ireceptor.org

python graph_airr_api.py v_call TRBV1,TRBV2,TRBV3,TRBV4,TRBV5,TRBV6,TRBV7 https://vdjserver.org/airr

 python graph_airr_api.py junction_length 30,33,36,39,42,45,48,51,54,57,60 https://vdjserver.org/airr

To run the generic heatmap plot:

python heatmap_api.py v_call j_call TRBV1,TRBV2,TRBV3,TRBV4,TRBV5,TRBV6,TRBV7 TRBJ1,TRBJ2,TRBJ3,TRBJ4,TRBJ5,TRBJ6,TRBJ7 http://turnkey-test2.ireceptor.org

python heatmap_api.py v_call j_call IGHV1,IGHV2,IGHV3,IGHV4,IGHV5,IGHV6,IGHV7 IGHJ1,IGHJ2,IGHJ3,IGHJ4,IGHJ5,IGHJ6,IGHJ7 http://turnkey-test2.ireceptor.org

## Using the API with 'curl'

The unix command line tool curl is a useful tool to query repositories using both the iReceptor and the AIRR APIs. Curl allows you to build API calls in the following way:
```
curl -k -X POST  -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" http://turnkey-test2.ireceptor.org/v2/samples
```
This curl command does the following
* It queries the web server at http://turnkey-test2.ireceptor.org
* The query request uses the /v2/samples API entry point to make the query
* It sets the headers for the request to let it know that the response is JSON and that the content being sent is "x-www-form-urlencoded" (required, but not explained!)
* It initiates the request as a POST request (most requests are either HTTP POST or GET requests)
* It allows insecure transactions (-k), again required and not explained...

In order to view the response from this command in a form that is a little easier to read, it is possible to use the python json.tool module.

```
curl -k -X POST  -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded"  http://turnkey-test2.ireceptor.org//v2/samples | python -m json.tool
```

Finally, if you want to look at the annotated sequences and their rearrangement features, you can use the /v2/sequence_summary API entry point. This returns both a summary of the samples that are found as well as a small, representative subset of the data that fits the search criteria. The query below searches for all of the sequence annotations from a single "sample=1" by specifying ```-d "ir_project_sample_id_list[]=1"```

```
curl -k -X POST  -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "ir_project_sample_id_list[]=1"  http://turnkey-test2.ireceptor.org//v2/sequences_summary
```
If you want to search for a specific rearrangement feature (a specific v_call) you can provide that as a parameter in the form of the parameter ```-d "v_call=IGHV1"```
```
curl -k -X POST  -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "ir_project_sample_id_list[]=1"  -d "v_call=IGHV1" http://turnkey-test2.ireceptor.org//v2/sequences_summary
```
If you want to download the data, you can use the following API call:
```
curl -k -X POST  -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "ir_project_sample_id_list[]=1" -d "output=tsv" -d "ir_data_format=airr"  http://turnkey-test2.ireceptor.org//v2/sequences_data > $filename
```

This entry point takes the following parameters:
* ```-d "output=tsv"``` - specifies that the type of data (tab delimited file).
* ```-d "ir_data_format=airr"``` - specify that the contents of the file format is AIRR compliant data.

