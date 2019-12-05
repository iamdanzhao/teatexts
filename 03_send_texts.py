# 03_send_texts.py
# contains code to send text messages to subjects

import numpy as np
import pandas as pd
from twilio.rest import Client

account_sid = 'TWILIO_ACCOUNT_SID'
auth_token = 'TWILIO_AUTH_TOKEN'
client = Client(account_sid, auth_token)

source_number = 'TWILIO_SOURCE_NUMBER'

def send_sms(msg, source, to):
    """Sends a text message. Returns 1 if success, 0 if failure."""
    try:
        message = client.messages \
            .create(
                body=msg,
                from_=source,
                to=to
            )
        return 1
    except:
        return 0     
    
def send_mms(msg, source, to, media):
    """Sends a text message. Returns 1 if success, 0 if failure."""
    try:
        message = client.messages \
            .create(
                body=msg,
                from_=source,
                to=to,
                media_url=media
            )
        return 1
    except:
        return 0

def send_messages(df, msg, source, img_url):
    """
    Sends text messages for a dataframe of subjects.

    Parameters:
    df (pd.DataFrame): dataframe of subjects, one per row
    msg (string): Message to send them. The URL will be appended to the end of this message.
    source (string): source phone number, configured through Twilio
    img_url (string): URL to an image, to be included only for subjects assigned to treatment

    Returns:
    pd.DataFrame: the input df, with an additional column indicating success or failure.
    """
    success = []
    
    for i, row in df.iterrows():
        if row['Treatment'] == 0:
            result = send_sms(msg + 'http://'+ row['Shortlink'] + ".", source, row['Phone'])
            success.append(result)
        elif row['Treatment'] == 1:
            result = send_mms(msg + 'http://'+ row['Shortlink'] + ".", source, row['Phone'], img_url)
            success.append(result)
        else:
            success.append(0)
    
    df['Success'] = np.array(success)
    
    return df

### EXAMPLE USAGE 1: send a welcome text

welcome_text = 'Welcome to TeaTexts, a new way to stay updated about the latest residential college teas. Please note that TeaTexts is currently in pilot phase. Reply STOP to unsubscribe.'

# read in the original cleaned csv
numbers = pd.read_csv('../Data/02_responses_cleaned.csv')

# make phone numbers into the required format for twilio by adding the "+1"
recipients = '+1' + numbers['Phone'].astype(str)
print(recipients.head())

# send texts
success = []
for recipient in recipients:
    result = send_sms(welcome_text, source_number, recipient)
    success.append(result)

# did they succeed?
np.mean(np.array(success))

### EXAMPLE USAGE 2: send one round of texts

msg_txt_a = 'TeaTexts: Tomorrow (Wed, 12 Nov 2019), there will be a tea with Weili Cheng and Ann Fraser Keating. Weili Cheng is Executive Director of the Yale Alumni Association (YAA) and holds a law degree from Georgetown University. Anne Fraser Keating holds an MBA from UPenn Wharton School and is the founder of Fraser Keating Associates, LLC. For details, time, and location, see '
img_url_a = 'http://teatexts.me/20191113-cheng-keating/cheng-keating.jpg'

# read in subjects and assignments
assignments_a = pd.read_csv('../Data/03_assignments_a.csv')

# this line actually sends out all 332 texts, so only run it once!
assignments_a_indicators = send_messages(
    df=assignments_a,
    msg=msg_txt_a,
    source=source_number,
    img_url=img_url_a
)

# write the indicators to a csv
assignments_a_indicators.to_csv("../Data/04_assignments_sent_a.csv")