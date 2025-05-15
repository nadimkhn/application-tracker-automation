#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Setting up the environment

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.discovery import build
import pandas as pd
from clean_column_names import clean_column_names
from datetime import datetime


# In[ ]:


# Configuration

SERVICE_ACCOUNT_FILE = '/Users/nadee/Desktop/PROJECTS/application-tracker-automation/secrets/vidhya-etl-dabd5ec76159.json'  # Path to your downloaded JSON file
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/drive']  # Read & write scope
SPREADSHEET_ID = '1Y8VlU05ekfbwExSMjp0fuCxXJOgKMyvtCUt3c3jFfIc'  # From the URL between /d/...../edit
RANGE_NAME = 'Sheet1'  # Adjust as needed


# In[ ]:


# Authenticate

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes = SCOPES)

sheets_service = build('sheets', 'v4', credentials = creds)
drive_service  = build('drive', 'v3', credentials = creds)


# In[ ]:


# Read Data
sheet = sheets_service.spreadsheets()
result = sheet.values().get(spreadsheetId = SPREADSHEET_ID,
                            range = RANGE_NAME).execute()
values = result.get('values', [])


# In[ ]:


# Convert to Dataframe
if not values:
    print("No data found.")
else:
    job_tracker = pd.DataFrame(values[1:], columns=values[0])  # Skip header row
    job_tracker.head()


# In[ ]:


# Make a copy of the data

job_tracker_cp = job_tracker.copy()


# In[ ]:


# Clean column names

clean_column_names(job_tracker_cp)


# In[ ]:


# Rename columns & drop rows with null values

job_tracker_cp.rename(columns = {'application_number':'unique_id'}, inplace = True)

job_tracker_cp.dropna(subset = ['role'], inplace = True)

# Reset index 

job_tracker_cp.reset_index(drop = True, inplace = True)


# In[ ]:


job_tracker_cp['dw_last_updated'] = str(datetime.now())


# In[ ]:


# Convert dataframe to a list of lists

values = [job_tracker_cp.columns.to_list()] + job_tracker_cp.values.tolist()


# In[ ]:


# Destination Sheet

DESTINATION_SHEET_ID = '1_hUXV_dGfWpPaV2GJVmcrJjOfHMVRJp36CxEw8eX3RQ'

# Clear the existing data

sheets_service.spreadsheets().values().clear(
    spreadsheetId = DESTINATION_SHEET_ID,
    range = 'Sheet1',
    body = {}
).execute()

# Write the transformed data

sheets_service.spreadsheets().values().update(
    spreadsheetId = DESTINATION_SHEET_ID,
    range = 'Sheet1!A1',
    valueInputOption = 'USER_ENTERED',
    body={'values': values}
).execute()

# SHARE NEW SHEET ACCESS TO MYSELF

drive_service.permissions().create(
    fileId=DESTINATION_SHEET_ID,
    body={
        'type': 'user',
        'role': 'writer',  # or 'reader'
        'emailAddress': 'nadimkhn323@gmail.com'
    },
    sendNotificationEmail=True
).execute()


# In[ ]:




