Due to the large size of czi files, we only include a sample dataset here to showcase
the algorithm with our sample code. But the complete code and the final results are also 
included here.

---------------------------------------------------------------------------------
Data sets

With this repo we also include an example file which user can play around to see
how the algorithm works. The user needs to execute timeseries_extraction_example.py
The link to the example file is:
https://data-proxy.ebrains.eu/api/permalinks/ebf8dacd-91ad-446b-a073-61750c513b71


The results after processing are saved in a pickled dictionary file bearing the name
dcEF-calcium-CA1_diff_mask_std3. One needs to use pickle library to load the data.
The data is stored in a dictionary which contains results from all experiment types,
conditions and cultures. One need to iterate over nested keys to get timeseries data
for every neuron for a given culture. The link to the result file is:
https://data-proxy.ebrains.eu/api/permalinks/b83ec1af-4b1f-4ca6-bf70-ca9614fd9a13
--------------------------------------------------------------------------------
