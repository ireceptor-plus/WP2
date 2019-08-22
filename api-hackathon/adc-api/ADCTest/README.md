This directory contains a testing code suite for the ADC API

# Testing approach

- Python code to run a single test
- Bash script to run a suite of tests and report results.

## Running the tests

```
python test_airr_api.py https://airr-api.ireceptor.org/airr/v1 repertoire repertoire/query2_repertoire.json
```
Run the python test code on the API base URL given, using the repertoire endpoint and the JSON query file in  ```repertoire/query2_repertoire.json```
