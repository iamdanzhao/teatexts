# 02_assign_shortlinks.py
# generates shortlink for each user using Rebrand.ly API, then assign to treatment/control
# to be used each time an experiment is run (i.e. for each A/B test we run, run this code)

import pandas as pd
import numpy as np

import requests
import json

def generate_shortlink(url):
    """
    Generates shortlink for input URL using Rebrand.ly API.

    Parameters:
    url (string): the URL to shorten

    Returns:
    string: a short URL
    """
    # parameters from rebrandly
    short_url_domain = 'go.teatexts.me'
    api_key = 'YOUR_API_KEY_HERE'

    # payloads for the API call
    linkRequest = {
        'destination': url,
        'domain': {
            'fullName': short_url_domain
        }
        # 'slashtag': 'TEXT_HERE'
    }

    # request headers for the api call
    requestHeaders = {
        'Content-type': 'application/json',
        'apikey': api_key
    }
    
    # make the api call to generate the link
    r = requests.post('https://api.rebrandly.com/v1/links',
                      data = json.dumps(linkRequest),
                      headers = requestHeaders)
    
    # return the shortlink, plus error handling
    if (r.status_code == requests.codes.ok):
        link = r.json()
        return link["shortUrl"]
    else:
        return "Error"

def assign_shortlinks(df, url, p, label):
    """
    Assigns unique shortlinks and treatment/control for a dataframe of observations.

    Parameters:
    df (pd.DataFrame): a dataframe with one row per observation
    url (string): the URL that all of the unique shortlinks should point to
    p (float): probably of assignment to treatment, to be passed into np.random.binomial
    label (string): name of the experiment, generally a letter

    Returns:
    pd.DataFrame: a dataframe of observations, plus the generated shortlinks and treatment assignment.
    """
    n = len(df)
    
    df['Shortlink'] = [generate_shortlink(url) for i in np.arange(n)]
    df['Treatment'] = np.random.binomial(1, p, n)
    df['Experiment'] = label
    df = df[['Phone', 'Shortlink', 'Treatment', 'Experiment']]
    
    return df

### EXAMPLE USAGE ---

# read in cleaned responses
responses = pd.read_csv("../Data/02_responses_cleaned.csv")
responses.head()

# apply the functions
assignments_a = assign_shortlinks(responses, 'http://teatexts.me/20191113-cheng-keating', 0.5, 'A')
assignments_a.to_csv("../Data/03_assignments_a.csv", index=False)