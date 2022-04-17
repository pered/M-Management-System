from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build

import logging

from typing import List, Optional, Tuple, Union

class SettingsCFG: 
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SAMPLE_SPREADSHEET_ID = "1odCeDDEq_1jmhz5XG1B9QbdBZ9RXwKZ8eJPLsv3KtkI"
    
    #Variables refering to methods for cloud sheets manipulation
    creds = service_account.Credentials.from_service_account_file(\
            'maximal-copilot-343018-f149332a7912.json',scopes=SCOPES)
    sheet = build('sheets','v4', credentials=creds).spreadsheets()   
    
    max_reg_per_user:int = 0
        
    def __init__(self) -> None:
        pass

    @classmethod
    def load(cls):
        logging.info("Initializing settings from settings sheet")
        results = SettingsCFG.sheet.values().get(spreadsheetId = SettingsCFG.SAMPLE_SPREADSHEET_ID, range = 'Settings').execute()
        SettingsCFG.max_reg_per_user = int(results['values'][0][1])
        logging.info("Initialised settings from settings sheet")
    