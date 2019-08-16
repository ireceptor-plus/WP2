import urllib.request, urllib.parse
import argparse
import json
import os, ssl
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

def getRearrangement(rearrangement_url, header_dict, query_dict={}):
    # Build the required JSON data for the post request. The user
    # of the function provides both the header and the query data

    # Convert the query dictionary to JSON
    query_json = json.dumps(query_dict)

    # Encode the JSON for the HTTP requqest
    query_json_encoded = query_json.encode('utf-8')

    # Try to make the connection and get a response.
    try:
        request = urllib.request.Request(rearrangement_url, query_json_encoded, header_dict)
        response = urllib.request.urlopen(request)
        url_response = response.read().decode(response.headers.get_content_charset())
    except urllib.error.HTTPError as e:
        print('Error: URL = ' + rearrangement_url)
        print('Error: Server could not fullfil the request')
        print('Error: Error code =', e.code)
        print(e.read())
        return json.loads('[]')
    except urllib.error.URLError as e:
        print('Error: URL = ' + rearrangement_url)
        print('Error: Failed to reach the server')
        print('Error: Reason =', e.reason)
        return json.loads('[]')
    
    # Convert the response to JSON so we can process it easily.
    json_data = json.loads(url_response)
    
    # Return the JSON of the results.
    return json_data

def getRepertoire(repertoire_url, header_dict, query_dict={}):
    # Build the required JSON data for the post request. The user
    # of the function provides both the header and the query data

    # Convert the query dictionary to JSON
    query_json = json.dumps(query_dict)

    # Encode the JSON for the HTTP requqest
    query_json_encoded = query_json.encode('utf-8')

    # Try to connect the URL and get a response. On error return an
    # empty JSON array.
    try:
        request = urllib.request.Request(repertoire_url, query_json_encoded, header_dict)
        response = urllib.request.urlopen(request)
        url_response = response.read().decode(response.headers.get_content_charset())
    except urllib.error.HTTPError as e:
        print('Error: Server could not fullfil the request')
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

def getQuery(query_key, query_value):
    # Buld the query dictionary according to the AIRR API standard
    rearrangement_query = {
        "filters": {
              "op":"=",
              "content": {
                "field":str(query_key),
                "value":query_value
              }
        },
        "facets":"repertoire_id"
    }

    return rearrangement_query


def performQueryAnalysis(base_url, query_key, query_values):
    # Ensure our HTTP set up has been done.
    initHTTP()
    # Get the HTTP header information (in the form of a dictionary)
    header_dict = getHeaderDict()

    # Select the API entry points to use, based on the base URL provided
    repertoire_url = base_url+'/v1/repertoire'
    rearrangement_url = base_url+'/v1/rearrangement'

    data = dict()
    graph_total = 0
    # Iterate over the query values of interest. One query per value gives us results
    # for all repertoires so this is about as efficient as it gets.
    for value in query_values:
        # Create the query for this value. Our query is a query on the value of interest
        # aggregated by repertoire_id. This gives us a list of values per repertoire.
        query_dict = getQuery(query_key, value)
        print('Performing query: ' + str(query_key) + ' = ' + str(value))
        print(query_dict)
        # Perform the query.
        query_json = getRearrangement(rearrangement_url, header_dict, query_dict)
        # Extract the "Rearrangement" component of the JSON response.
        rearrangement_json = query_json["Rearrangement"]
        # Because we aggregated via repertoire_id, we need to iterate over the
        # repertoires returned and sum up their count.
        total = 0
        for repertoire in rearrangement_json:
           total = total + repertoire['count']
        # Store the total value in our data dictionary for this key.
        data.update({value:total})
        graph_total = graph_total + total
        print("Total for " + query_key + "/" + value + " = " + str(total))

    # Finally, dump out the actual data we are going to graph...
    print('\nGraph data overview - ' + query_key + ':')
    for key, value in data.items():
        print(str(key) + ' = ' + str(value))
    print('graph total = ' + str(graph_total))
    return data

def plotData(plot_names, plot_data, title, filename):
    # Set up the plot
    plt.rcParams.update({'figure.autolayout': True})
    fig, ax = plt.subplots() 
    # Remove warning
    fig.set_tight_layout(False)
    # Make it a bar graph using the names and the data provided
    ax.barh(plot_names, plot_data)
    ax.set_title(title)

    # Write the graph to the filename provided.
    fig.savefig(filename, transparent=False, dpi=240)
    print('Saved image in ' + filename)


def getArguments():
    # Set up the command line parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=""
    )

    # Field in the API to use for the histogram
    parser.add_argument("api_field")
    # Values to search for in the field to generate the histogram
    parser.add_argument("graph_values")
    # The URL for the repository to search
    parser.add_argument("base_url")
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
    values = options.graph_values.split(',')
    # Perform the query analysis, gives us back a dictionary.
    data = performQueryAnalysis(options.base_url, options.api_field, values)
    sorted_data = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
    # Graph the results
    title = options.base_url + " " + options.api_field
    url_info = urllib.parse.urlparse(options.base_url)
    filename = url_info.netloc + "-" + options.api_field + ".png"
    plotData(list(sorted_data.keys()), list(sorted_data.values()), title, filename)

    # Return success
    sys.exit(0)

