from typing import Optional, Tuple, Dict, List
from pandas import Series, DataFrame
from .ext import Sheets
import logging
import json

class UserList(Sheets, list['User']): 

    SPREADSHEET_ID = "10bzoC_M0GOyEB8CH5zY9EXE7tGtxnC8vwJO3tTBDkyA"
    sheet_info = [{"Range": "Wholesale",
                    "sheetID": 0},
                  {"Range": "Admin",
                    "sheetID": 1929008158}]
    
    request_list:List = []
    
    def __init__(self):
        super().__init__(write_sheet=True)
        
    def load(self):
        if UserList.__len__ != 0:
            UserList.clear(self)
            logging.info("Reloaded product list")
        
        self.results = Sheets.load(self)
        
        df = DataFrame(self.results['valueRanges'][0]['values'][1:], columns = self.results['valueRanges'][0]['values'][0])


class User:
    all_users = UserList()
    
    def __init__(self, df:Tuple[int, Series] = (None, Series(dtype=(float))), sheetID:int = None):
        try:
            self.firstName:str = df[1]['First Name']
        except:
            self.firstName:str = str()
            
        try: 
            self.lastName:str = df[1]['Last Name']
        except:
            self.lastName:str = str()
            
        try:
            self.mmsUserID:str = df[1]['MMS UserID']
        except:
            self.mmsUserID:str = str()
            
        try:
            self.telegramUserID:str = df[1]['Telegram UserID']
        except:
            self.telegramUserID:str = str()
        
        try:
            self.access:str = df[1]['Access']  
        except:
            self.access:str = str()
        
        self.metadataId:str = int()
        
        if sheetID != None:
            User.all_users.request_list += [{"createDeveloperMetadata": \
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
    
    @property
    def metadataId(self) -> int:
        return self._metadataId

        
    @metadataId.setter
    def metadataId(self, metadataId:int) -> None:
        self._metadataId = metadataId
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
        
    def save(self)-> None:
        batch_datafilter_update = {"valueInputOption": 'USER_ENTERED',
                                    "data": [{"dataFilter": {'developerMetadataLookup': 
                                                            {'metadataId': self.metadataId
                                                            }},
                                    "majorDimension": 'ROWS',
                                    "values": [[self.mmsUserID, self.firstName, self.lastName, self.telegramUserID, self.access]
                                                ]}]}
            
        User.all_users.sheet.values().batchUpdateByDataFilter(spreadsheetId=User.all_users.SAMPLE_SPREADSHEET_ID, body=batch_datafilter_update).execute()
        
    def refresh(self) -> None:
        batch_request_get = {

            'data_filters': [{'developerMetadataLookup': {'metadataId': self.metadataId
                                                          }}]  # TODO: Update placeholder value.

        }
        
        response =  User.all_users.sheet.values().batchGetByDataFilter(spreadsheetId= User.all_users.SAMPLE_SPREADSHEET_ID, body = batch_request_get).execute()
        self.mmsUserID,self.firstName,self.lastName,self.telegramUserID,self.access = response['valueRanges'][0]['valueRange']['values'][0][0:5]
        


class Admin(User):
    def __init__(self, df:Tuple[int, Series] = (None, Series(dtype=(float))), sheetID:int = None):
        super().__init__(df, sheetID)

class WholesaleUser(User):
    def __init__(self, df:Tuple[int, Series] = (None, Series(dtype=(float))), sheetID:int = None):
        super().__init__(df, sheetID)
        try:
            pass
            #self.business:Business = BusinessList.search(df[1]['Assigned Business'],"MMS Business ID")[0]
        except:
            pass
            #self.business:Business = None