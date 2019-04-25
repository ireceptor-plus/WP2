# Hackathon instructions

## Logging in to Jupyter

We have worked with our collaborators at the Pacific Institute of Mathematical Sciences (PIMS - https://www.pims.math.ca/) to set up a Jupyter environment for iReceptor (called Syzygy). The Jupyter notebooks run on Compute Canada's infrastructure (www.computecanada.ca) You can access this environment here: https://ireceptor.syzygy.ca/

Authentication to the Jupyter notebooks have been configured to use your GitHub user accounts, so you will need to have a GitHub account to participate. Currently, the iReceptor Jupyter environment is set up so that anyone can log in.

To log in to Jupyter, simply go to: https://ireceptor.syzygy.ca/ and click on the log in icon. If you are already logged in to your GitHub account, it will ask you if you are OK to share your information with Syzygy. Choose yes (assuming you are) and you will be logged in to Jupyter.

## Setting things up

In order to use the Jupyter environment for the iReceptor Plus hackathon, you will need to configure a few things.

1. Open a "Terminal" in the Jupyter environment: To do this, use the "New" menu in the top right and choose "Terminal". This will give you a Unix command line tab in your browser.
1. Clone the WP2 git repository: In the Terminal, type the Git clone command "git clone https://github.com/ireceptor-plus/WP2.git".
1. Install the AIRR python module: In the Terminal, type the python PIP command to download and install the AIRR python module as follows "pip install airr"
1. Create a data working directory: This is not absolutely necessary, but you might want to put all of your hackathon data into a single directory (creating subdirectories as required). You can do this as you normally would at the Unix command line (e.g. mkdir data).

## Running the code

There are four very basic applications that have been created as a "starting point" for the hackathon. The focus of the hackathon is to explore the various ways of interacting with an AIRR repository. There are two fundamental ways of doing this, using the Web API to perform queries and using the query results to perform analysis or downloading an AIRR TSV file and performing analyses on the downloaded data.

### Using the Web API

There are two simple python analysis applications that have been created that use the iReceptor API to query a repository and perform an anlaysis. The two applications are a simple "histogram" application and a simple "heatmap" application.

To run the histogram application, simply type the following:

```
python3 ~/WP2/api-hackathon/graph_api.py v_call IGHV1,IGHV2,IGHV3,IGHV4,IGHV5,IGHV6,IGHV7,IGHV8,IGHV9,IGHV10 http://turnkey-test2.ireceptor.org
```
Where:
- v_call is the AIRR field on which you want the histogram to be performed.
- IGHV1 ... are the list of histogram bins that you want to use. The application will count the frequency of the appearance of that value in the repository.
- http://turnkey-test2.ireceptor.org is the repository to query.

To run the heatmap application, simply type the following:

```
python3 ~/WP2/api-hackathon/heatmap_api.py v_call j_call IGHV1,IGHV2,IGHV3,IGHV4,IGHV5,IGHV6,IGHV7,IGHV8 IGHJ2,IGHJ3,IGHJ4 http://turnkey-test2.ireceptor.org
```
Where
- v_call is the AIRR field that you want to appear on the X axis of the heatmap.
- j_call is the AIRR field that you want to appear on the Y axis of the heatmap.
- IGHV1 ... are the bins that you want to use on the X axis. The application will count the frequency of the appearance of that value in the repository for each of the bins on the Y axis.
- IGHJ1 ... are the list of bins that you want to use on the Y axis. The application will count the frequency of the appearance of that value in the repository for each of the bins on the X axis.
- http://turnkey-test2.ireceptor.org is the repository to query.

### Downloading AIRR TSV using the Web API

Two similar python analysis applications (and shell scripts) have been created that use the iReceptor API to download an AIRR TSV file and then perform the analysis on the AIRR TSV file. The python applications are supported by shell scripts that perform some pre-processing on the AIRR TSV files to prepare them for analysis. Note that the AIRR TSV analysis works on a single sample only. The shell script uses the Web API to query the repository for all of the data for a single sample, downloads the data for that sample, and then performs the analysis. There is a "helper" shell script available for searching for Database IDs for a sample.

To run the histogram application, simply type the following:

```
~/WP2/airr-hackathon/run_histogram.sh 1 v_call http://turnkey-test2.ireceptor.org
```
Where:
- "1" is the Database ID for a single sample.
- "v_call" is the AIRR field on which you want the histogram to be performed.
- http://turnkey-test2.ireceptor.org is the repository to query.

To run the heatmap application, simply type the following:

```
~/WP2/airr-hackathon/run_heatmap.sh 9 http://turnkey-test2.ireceptor.org
```
Where
- "9" is the Database ID for a single sample.
- http://turnkey-test2.ireceptor.org is the repository to query.

## Exploring the samples in a repository

There is also a simple bash shell script that will allow you to query a repository and extract the "Repertoire Metadata" in a repository.

To run the sample shell script, simply type:

```
~/WP2/airr-hackathon/get_samples.sh http://turnkey-test2.ireceptor.org
```

This will return a JSON response for all of the Repertoires in the given repository.

If you want to look at a specific AIRR field in the Repertoire Metadata simply use "grep" to filter for the AIRR term of interest.

```
~/WP2/airr-hackathon/get_samples.sh http://turnkey-test2.ireceptor.org | egrep "study_title|study_id"
```