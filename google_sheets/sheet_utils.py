"""
A helper class to read content from individual sheets withing a .gsheet file.
Requires:
- A credentials.json file containing your API-based credentials
- A pickle file containing the access token
Guide --> https://developers.google.com/sheets/api/quickstart/python
"""

import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import logging
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
import pandas as pd


class Sheet_Utils():
    
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.STRUCTURE = {}

    
    #Function to get Google Sheet Credentials
    def gsheet_api_check(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds
    
    
    
    def pull_sheet_data(self, spreadsheet_id, sheets_list):
    
        """
        Args:

        - spreadsheet_id: the spreadsheet from which you want to read data. 
        Id is contained within your gsheet url, in the following fashion 
          --> https://docs.google.com/spreadsheets/d/{spreadsheet_id}

        - sheets_list: A list-like element containing the sheet names within your file.
          --> ['Sheet 1', 'Sheet 2']

        Returns:
          STRUCTURE -> A dictionary of dataframes, each containing data for the read sheets.

        """
        creds = self.gsheet_api_check()
        service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
        active_sheet = service.spreadsheets()
               
        for sheet_name in sheets_list:
            result = active_sheet.values().get(
                spreadsheetId = spreadsheet_id,
                range=sheet_name).execute()
            values = result.get('values', [])

            rows = active_sheet.values().get(spreadsheetId=spreadsheet_id, 
                                          range=sheet_name).execute()
            data = rows.get('values')
            data = pd.DataFrame(data[1:], columns=data[0])
            
            self.STRUCTURE[sheet_name] = data

        return self.STRUCTURE
