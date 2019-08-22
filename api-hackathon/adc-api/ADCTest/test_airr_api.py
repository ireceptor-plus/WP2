import urllib.request, urllib.parse
import argparse
import json
import os, ssl
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

def processQuery(query_url, header_dict, query_dict={}):
    # Build the required JSON data for the post request. The user
    # of the function provides both the header and the query data

    # Convert the query dictionary to JSON
    query_json = json.dumps(query_dict)

    # Encode the JSON for the HTTP requqest
    query_json_encoded = query_json.encode('utf-8')

    # Try to connect the URL and get a response. On error return an
    # empty JSON array.
    try:
        request = urllib.request.Request(query_url, query_json_encoded, header_dict)
        response = urllib.request.urlopen(request)
        url_response = response.read().decode(response.headers.get_content_charset())
    except urllib.error.HTTPError as e:
        print('Error: Server could not fullfil the request to ' + query_url)
        print('Error: Error code =', e.code)
        print(e.read())
        return json.loads('[]')
    except urllib.error.URLError as e:
        print('Error: Failed to reach the server')
        print('Error: Reason =', e.reason)
        return json.loads('[]')

    # Convert the response to JSON so we can process it easily.
    json_data = json.loads(url_response)

    # Return the JSON data
    return json_data

def getHeaderDict():
    # Set up the header for the post request.
    header_dict = {'accept': 'application/json',
                   'Content-Type': 'application/json'}
    return header_dict

def initHTTP():
    # Deafult OS do not have create cient certificate bundles. It is
    # easiest for us to ignore HTTPS certificate errors in this case.
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)): 
        ssl._create_default_https_context = ssl._create_unverified_context

def testAPI(base_url, entry_point, query_files, verbose, force):
    # Ensure our HTTP set up has been done.
    initHTTP()
    # Get the HTTP header information (in the form of a dictionary)
    header_dict = getHeaderDict()

    # Build the full URL combining the URL and the entry point.
    query_url = base_url+'/'+entry_point

    # Iterate over the query files
    for query_file in query_files:
        # Open the JSON query file and read it as a python dict.
        try:
            with open(query_file, 'r') as f:
                query_dict = json.load(f)
        except IOError as error:
            print("ERROR: Unable to open JSON file " + query_file + ": " + str(error))
            return 0
        except json.JSONDecodeError as error:
            if force:
                print("Warning: JSON Decode error detected in " + query_file + ": " + str(error))
                with open(query_file, 'r') as f:
                    query_dict = f.read().replace('\n', '')
            else:
                print("ERROR: JSON Decode error detected in " + query_file + ": " + str(error))
                return 0
        except Exception as error:
            print("ERROR: Unable to open JSON file " + query_file + ": " + str(error))
            return 0
            
        if verbose:
            print('Performing query: ' + str(query_dict))

        # Perform the query.
        query_json = processQuery(query_url, header_dict, query_dict)
        if verbose:
            print('Query response: ' + str(query_json))

        # Print out an error if the query failed.
        if len(query_json) == 0:
            print('ERROR: Query file ' + query_file + ' to ' + query_url + ' failed')
            return 0

        # Extract the "Rearrangement" component of the JSON response.
        #rearrangement_json = query_json["Rearrangement"]
        # Because we aggregated via repertoire_id, we need to iterate over the
        # repertoires returned and sum up their count.
        #total = 0
        #for repertoire in rearrangement_json:
        #   total = total + repertoire['count']
        # Store the total value in our data dictionary for this key.
        #data.update({value:total})
        #graph_total = graph_total + total
        #print("Total for " + query_key + "/" + value + " = " + str(total))
        print('Query file ' + query_file + ' to ' + query_url + ' OK')

    return 1

def getArguments():
    # Set up the command line parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=""
    )

    # The URL for the repository to test
    parser.add_argument("base_url")
    # The API entry point to use
    parser.add_argument("entry_point")
    # Comma separated list of query files to test.
    parser.add_argument("query_files")
    # Force JSON load flag
    parser.add_argument(
        "-f",
        "--force",
        action="store_const",
        const=True,
        help="Force sending bad JSON even when the JSON can't be loaded.")
    # Verbosity flag
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Run the program in verbose mode.")

    # Parse the command line arguements.
    options = parser.parse_args()
    return options


if __name__ == "__main__":
    # Get the command line arguments.
    options = getArguments()
    # Split the comma separated input string.
    query_files = options.query_files.split(',')
    # Perform the query analysis, gives us back a dictionary.
    data = testAPI(options.base_url, options.entry_point, query_files, options.verbose, options.force)
    # Return success
    sys.exit(0)

