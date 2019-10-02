This directory contains a set of useful JSON queries using the AIRR Data Commons query API (ADC API).

# iReceptor API equivalents

Below you will find a description of a set of ADC API queries that are for the most part functionally equivalent to the older iReceptor API queries. 

## The /v2/samples equivalents

The iReceptor API /v2/samples API performs to functions, it searches for and returns the repertoire metadata for the set of samples that meet the search criteria provided as well as returns a count for the number of rearrangements for each sample. The ADC API can not perform this function in a single call, and therefore the equivalent must be done by two calls:

- the first call retrieves the repertoire metadata for the search criteria
- the second call usese the repertoire_ids and the facets capability to count the number of rearrangments in each repertoire_id. 

These two steps are captured by the following two curl commands, using the JSON query files in this directory.

```
curl -s --data @samples-step1-twofilters.json https://vdjserver.org/airr/v1/repertoire | python -m json.tool
```
This command searches the repertoires in the repository that match the filters provided. In this case, the search is for a specific subject_id ("TW05B") with a specific type of cell_subset ("Memory CD8+ T cell"). This returns the Repertoire Metadata for the query results, but does not provide a count of the rearrangements for each Repertoire.

In order to determine the rearrangement count for each Repertoire retreived, it is necessary to search for all of the rearrangements for each repertoire and aggregate them by repertoire_id using the facets capability of the ADC API. 
```
curl -s --data @samples-step2.json https://vdjserver.org/airr/v1/rearrangement | python -m json.tool
```

Combined, these two queries provide the equivalent information provide by the iReceptor /v2/samples API entry point.

## The /v2/sequences_summary equivalent

The iReceptor /v2/sequences_summary entry point has three response components, a summary of the query repsonse that contains the repertoire metadata, a count of the number of rearrangements for each repertoire, and a subset of the rearrangement data as a small sample of the overall response. The first two components of this response are almost identical as the /v2/samples. You acquire the repertiore metadata as follows:

```
curl -s --data @samples-step1-twofilters.json https://vdjserver.org/airr/v1/repertoire | python -m json.tool
```

Extracting the repertoire_id, one then needs to determine the count of the rearrangments that both meet the repertoire query (as indicated by the repertoire_ids) and the rearrangement query (for example, searching for a specific v_call such as "TRAV8-2*01"). This can be done as follows:

```
curl -s --data @sequences-step2-vcall.json https://vdjserver.org/airr/v1/rearrangement | python -m json.tool
```

Finally, to get a representative sample of the actual rearrangement data, one can request the actual rearrangement data by performing the same query with a ADC API "from" and "size" parameters as follows:

```
curl -s --data @sequences-step3-vcall.json https://vdjserver.org/airr/v1/rearrangement | python -m json.tool
```

Note: The current iReceptor test API is on https://airr-api.ireceptor.org/airr/v1/
