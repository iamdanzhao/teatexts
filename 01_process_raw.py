# 01_process_raw.py
# cleans and processes survey data from Google Forms

### IMPORT PACKAGES -----

import pandas as pd
import numpy as np

### READ AND CLEAN DATA -----

# read data
responses = pd.read_csv("../Data/01_responses.csv")

# rename columns
responses.columns = ['Time', 'Phone', 'Graduation', 'Pronouns', 'College', 'Area of study', 'Number of teas', 'Consent']

# remove timestamp and consent, no longer need those
responses = responses.drop(['Time', 'Consent'], axis=1)

# clean phone number (all phone numbers are 10-digit US numbers)
responses['Phone'] = responses['Phone'].str.replace('[^\d]+', '', regex=True)

# remove cases where they entered a '1'
responses['Phone'] = responses['Phone'].str.replace('^1', '')

# one row contained invalid phone number (text 'anise'), remove this row
responses = responses[responses['Phone'] != '']

# convert phone to numeric, since this will be our ID
responses['Phone'] = responses['Phone'].astype('int64')

### HANDLE DUPLICATE DATA -----

# view duplicate data
responses[responses.duplicated('Phone')]

# remove these rows
responses = responses[~responses.duplicated('Phone')]

### WRITE TO CSV -----

responses.to_csv("../Data/02_responses_cleaned.csv", index=False)