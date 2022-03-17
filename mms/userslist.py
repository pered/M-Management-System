from __future__ import print_function
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build

from typing import List, Optional
import pandas as pd
from .users import Admin, RetailUser

class UserList:
    adminList: List[Admin] = []
    retailList: List[RetailUser] = []
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SAMPLE_SPREADSHEET_ID = "10bzoC_M0GOyEB8CH5zY9EXE7tGtxnC8vwJO3tTBDkyA"
    ADMIN_SAMPLE_RANGE_NAME = 'Admin!A1:E'
    RETAIL_SAMPLE_RANGE_NAME = 'Retail!A1:E'
    
    creds = service_account.Credentials.from_service_account_file(\
            'maximal-copilot-343018-f149332a7912.json',scopes=SCOPES)
    
    adminSheet = build('sheets','v4', credentials=creds).spreadsheets()
    retailSheet = build('sheets','v4', credentials=creds).spreadsheets()    
        
    def __init__(self) -> None:
        pass
    
    def load(self) -> None:
        adminResults = UserList.adminSheet.values().get(spreadsheetId=\
                            UserList.SAMPLE_SPREADSHEET_ID, range=\
                                UserList.ADMIN_SAMPLE_RANGE_NAME).execute()
            
        retailResults = UserList.retailSheet.values().get(spreadsheetId=\
                            UserList.SAMPLE_SPREADSHEET_ID, range=\
                                UserList.RETAIL_SAMPLE_RANGE_NAME).execute() 
            
        admin_df = pd.DataFrame.from_dict(adminResults['values'])
        
        retail_df = pd.DataFrame.from_dict(retailResults['values'])
        