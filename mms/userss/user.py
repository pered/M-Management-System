from typing import Optional, Tuple, Dict
from pandas import Series
import logging
from .. import userslist
import json

class User:
    def __init__(self, df:Tuple[int, Series] = (None, Series(dtype=(float))), sheetID:int = None):
        try:
            self.firstName:str = df[1]['First Name']
        except:
            self.firstName:str = None
            
        try: 
            self.lastName:str = df[1]['Last Name']
        except:
            self.lastName:str = None
            
        try:
            self.mmsUserID:str = df[1]['MMS UserID']
        except:
            self.mmsUserID:str = None
            
        try:
            self.telegramUserID:str = df[1]['Telegram UserID']
        except:
            self.telegramUserID:str = None
        
        try:
            self.access:str = df[1]['Access']  
        except:
            self.access:str = None
        
        self.metadataId = None
        
        if sheetID != None:
            userslist.UserList.request_list += [{"createDeveloperMetadata": \
                                                 {"developerMetadata": {
                                                     "metadataKey": "sheetID"+f"{df[0]+1}",
                                                     "location" : {"dimensionRange":
                                                                   {"sheetId":sheetID,
                                                                    "dimension":"ROWS",
                                                                    "startIndex": df[0]+1,
                                                                    "endIndex": df[0]+2}
                                                                   },
                                                     "visibility": "DOCUMENT"}
                                                         }}]
        logging.info(f"Created {type(self)} user {self.firstName}")
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        
    def set_metadataId(self,metadataId:int) -> None:
        self.metadataId = metadataId
        
    def save(self)-> None:
        batch_datafilter_update = {"valueInputOption": 'USER_ENTERED',
                                    "data": [{"dataFilter": {'developerMetadataLookup': 
                                                            {'metadataId': self.metadataId
                                                            }},
                                    "majorDimension": 'ROWS',
                                    "values": [[self.mmsUserID, self.firstName, self.lastName, self.telegramUserID, self.access]
                                                ]}]}
            
        userslist.UserList.sheet.values().batchUpdateByDataFilter(spreadsheetId=userslist.UserList.SAMPLE_SPREADSHEET_ID, body=batch_datafilter_update).execute()
        
    def refresh(self) -> None:
        batch_request_get = {

            'data_filters': [{'developerMetadataLookup': {'metadataId': self.metadataId
                                                          }}]  # TODO: Update placeholder value.

        }
        
        response = userslist.UserList.sheet.values().batchGetByDataFilter(spreadsheetId=userslist.UserList.SAMPLE_SPREADSHEET_ID, body = batch_request_get).execute()
        self.mmsUserID,self.firstName,self.lastName,self.telegramUserID,self.access = response['valueRanges'][0]['valueRange']['values'][0][0:5]
        
