# 05_get_counts.py
# gets link counts for each shortlink using the Rebrandly API

import pandas as pd
import numpy as np

import requests
import json

### NOTES ON REBRANDLY API

# API reference: https://developers.rebrandly.com/reference#links-list-endpoint
#
# The list APIs endpoint has a limit of 25 links returned per calls, with an option to
# set the last link from the previous call. Thus, what I'm essentially doing is looping
# through "pages", saving the ID from the last link in each loop iteration, and then
# using that as the starting point in the next loop iteration.
#
# See here for more info on pagination: https://developers.rebrandly.com/docs/understanding-pagination
#
# I haven't tested the case where there's an exactly even number of pages (e.g. 2500, 2525, 
# 2550, etc. links), which may raise an error in the 2nd nested `for` loop — if this were 
# the case, need to fix to catch the error there.

# starting values
n_links = 2404
request_limit = 25
last = ''

# API call parameters
url = 'https://api.rebrandly.com/v1/links'
headers = {
    'content-type': 'application/json',
    'apikey': 'API_KEY_HERE'
}

# containers for informaion
ids = []
slashtags = []
shortUrls = []
n_clicks = []

# loop through
for i in np.arange(np.ceil(n_links / request_limit)):
    
    # note using the last parameter
    queryString = {
        'orderBy': 'createdAt',
        'orderDir': 'desc',
        'limit': '5000',
        'last': last
    }
    
    # make API call and convert to json
    response = requests.request("GET", url, headers=headers, params=queryString)
    json = response.json()
    
    # add properties of each item to the list
    # there's probably a more efficient way to do this (ex: convert json to dataframe, list comp, etc.)
    for item in json:
        ids.append(item['id'])
        slashtags.append(item['slashtag'])
        shortUrls.append(item['shortUrl'])
        n_clicks.append(item['clicks'])
    
    # save the ID of the last link to use in the next loop iteration
    last = json[-1]['id']
    
# save into dataframe
clicks = pd.DataFrame({
    'id': ids,
    'slashtag': slashtags,
    'shortUrl': shortUrls,
    'clicks': n_clicks
})

# write to csv
clicks.to_csv("../data/05_clicks.csv", index=False)