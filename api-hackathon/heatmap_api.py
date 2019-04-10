import urllib.request, urllib.parse
import argparse
import json
import os, ssl
import sys
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import OrderedDict

def getSequenceSummary(sequence_url, header_dict, query_dict={}):
    # Build the required JSON data for the post request. The user
    # of the function provides both the header and the query data
    url_dict = dict()
    #url_dict.update(header_dict)
    url_dict.update(query_dict)
    url_data = urllib.parse.urlencode(url_dict).encode()

    # Try to make the connection and get a response.
    try:
        request = urllib.request.Request(sequence_url, url_data, header_dict)
        #response = urllib.request.urlopen(sequence_url, data=url_data)
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
    
    # Print out the summary stats for the repository.
    sample_summary = json_data['summary']

    # Return the JSON of the results.
    return sample_summary

def getSamples(sample_url, header_dict, query_dict={}):
    # Build the required JSON data for the post request. The user
    # of the function provides both the header and the query data
    url_dict = dict()
    #url_dict.update(header_dict)
    url_dict.update(query_dict)
    url_data = urllib.parse.urlencode(url_dict).encode()

    # Try to connect the URL and get a response. On error return an
    # empty JSON array.
    try:
        request = urllib.request.Request(sample_url, url_data, header_dict)
        #response = urllib.request.urlopen(sample_url, data=url_data)
        response = urllib.request.urlopen(response)
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
    #print(url_response)
    json_data = json.loads(url_response)
    # Return the JSON data
    return json_data

def getHeaderDict():
    # Set up the header for the post request.
    header_dict = {'accept': 'application/json',
                   'Content-Type': 'application/x-www-form-urlencoded'}
    return header_dict

def initHTTP():
    # Deafult OS do not have create cient certificate bundles. It is
    # easiest for us to ignore HTTPS certificate errors in this case.
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)): 
        ssl._create_default_https_context = ssl._create_unverified_context

def performQueryAnalysis(base_url, query_xkey, query_ykey, query_xvalues, query_yvalues):
    # Ensure our HTTP set up has been done.
    initHTTP()
    # Get the HTTP header information (on the form of a dictionary)
    header_dict = getHeaderDict()

    # Select the API entry points to use, based on the base URL provided
    sample_url = base_url+'/v2/samples'
    sequence_url = base_url+'/v2/sequences_summary'

    # Create a numpy array (zeroed) of the correct size.
    data = np.zeros((len(query_yvalues), len(query_xvalues)))
    # Iterate over the query values of interest. One query per value gives us results
    # for all samples so this is about as efficient as it gets.
    # For each of the X query values
    xindex = 0
    for xvalue in query_xvalues:
        yindex = 0
        # For each of the Y query values
        for yvalue in query_yvalues:
            # Create the query dictinoary values
            query_dict = dict()
            query_dict.update({query_xkey: xvalue, query_ykey:yvalue})
            sequence_summary_json = getSequenceSummary(sequence_url, header_dict, query_dict)
            # Because we want the total count for all samples for each X,Y pair, we 
            # iterate over the samples and sum the count for each sample.
            for sample in sequence_summary_json:
                # Update the count for the sample we are considering
                data[yindex, xindex] = data[yindex, xindex] + sample['ir_filtered_sequence_count']
                print('   ' + query_xkey + '/' + str(xvalue) +
                      ' , ' + query_ykey + '/' + str(yvalue) +
                      ' ( ' + str(xindex) + ',' + str(yindex) + ' ) ' +
                      ' = ' + str(sample['ir_filtered_sequence_count']) +
                      ' , ' + str(data[yindex, xindex]))
            yindex = yindex + 1
        xindex = xindex + 1

    return data

def plotData(plot_data, xlabels, ylabels, title, filename):
    # Plot code borrowed from here: https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html

    matplotlib.use('Agg')
    fig, ax = plt.subplots()
    im = ax.imshow(plot_data)
    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Number of Annotations", rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xlabels)))
    ax.set_yticks(np.arange(len(ylabels)))
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    # ... and label them with the respective list entries
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels)
    ax.set_title(title)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                     rotation_mode="anchor")

    # Save the file in the filename provided
    fig.savefig(filename, transparent=False, dpi=240, bbox_inches="tight")

def getArguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=""
    )

    # Field in the API to use for x dimension of the heatmap
    parser.add_argument("api_xfield")
    # Field in the API to use for y dimension of the heatmap
    parser.add_argument("api_yfield")
    # Values of the x field to use for x dimension of the heatmap
    parser.add_argument("graph_xvalues")
    # Values of the y field to use for y dimension of the heatmap
    parser.add_argument("graph_yvalues")
    # URL to used for the search
    parser.add_argument("base_url")
    # Verbosity flag.
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Run the program in verbose mode. This option will generate a lot of output, but is recommended from a data provenance perspective as it will inform you of how it mapped input data columns into repository columns.")

    # Parse the options.
    options = parser.parse_args()
    return options


if __name__ == "__main__":
    # Get the command line arguments.
    options = getArguments()
    # Split the comma separated input string.
    xvalues = options.graph_xvalues.split(',')
    yvalues = options.graph_yvalues.split(',')
    # Perform the query analysis, gives us back a dictionary.
    data = performQueryAnalysis(options.base_url, options.api_xfield, options.api_yfield, xvalues, yvalues)
    # Graph the results
    title = options.api_xfield + " " + options.api_yfield + " Usage"
    filename = options.api_xfield + "_" + options.api_yfield + ".png"
    plotData(data, xvalues, yvalues, title, filename)

    # Return success
    sys.exit(0)

