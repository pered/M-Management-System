from __future__ import print_function, annotations
from google.oauth2 import service_account
from googleapiclient.discovery import build

import logging
from typing import List,Tuple,Dict, overload
from pandas import Series, DataFrame



class Sheets:
    sheet_info:List[Dict] = [{}]
    
    def __init__(self, write_sheet:bool = False):
        if write_sheet == True:
            self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            self.creds = service_account.Credentials.from_service_account_file(\
                    'maximal-copilot-343018-f149332a7912.json',scopes=self.SCOPES)
                
            self.sheet = build('sheets','v4', credentials=self.creds).spreadsheets()    
            
            delete_all = {"requests" : [{"deleteDeveloperMetadata":{"dataFilter": {\
            "developerMetadataLookup": {"metadataLocation": {"sheetId":product["sheetID"]}}}}} for product in self.sheet_info
                ]}
           
            self.sheet.batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=delete_all).execute()
        else:
            self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            self.creds = service_account.Credentials.from_service_account_file(\
                    'maximal-copilot-343018-f149332a7912.json',scopes=self.SCOPES)
                
            self.sheet = build('sheets','v4', credentials=self.creds).spreadsheets()   
    
    def load(self):
        return self.sheet.values().batchGet(spreadsheetId = self.SPREADSHEET_ID,\
                            ranges=[x["Range"] for x in self.sheet_info]).execute()
    
    def save(self):
        pass
