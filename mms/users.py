from typing import Optional, Tuple, Dict, List
from .ext import Sheets
import logging
import json
from pandas import DataFrame, Series

class UserList(Sheets, list['User']): 

    SPREADSHEET_ID = "10bzoC_M0GOyEB8CH5zY9EXE7tGtxnC8vwJO3tTBDkyA"
    sheet_info = [{"Range": "Wholesale",
                    "sheetID": 0},
                  {"Range": "Admin",
                    "sheetID": 1929008158}]
    
    request_list:List = []
    
    def __init__(self):
        super().__init__(write_sheet=True)
        #Delete all previous metadata from users sheets, reference to Wholesale and Admin sections
        logging.info("Initializing users from user sheet")
        delete_all = {"requests" : [
            {"deleteDeveloperMetadata":{"dataFilter": {\
            "developerMetadataLookup": {"metadataLocation": {"sheetId":sheets["sheetID"]}}}}} for sheets in self.sheet_info 
            ]}
        self.sheet.batchUpdate(spreadsheetId=UserList.SPREADSHEET_ID, body=delete_all).execute()
        logging.info("Initialised users from user sheet")
        
    def load(self):
        if UserList.__len__ != 0:
            UserList.clear(self)
            logging.info("Reloaded product list")
        
        self.results = Sheets.load(self)
        
        #Create a list of objects with products in them
        [[User(UserList.sheet_info[index]['Range'], UserList.sheet_info[index]['sheetID'], sf_user)
          for sf_user in df_user.iterrows()] 
             for index, df_user in [(self.results['valueRanges'].index(userRange),DataFrame(userRange['values'][1:], columns = userRange['values'][0])) 
                                       for userRange in self.results['valueRanges']]]
        
        response = self.sheet.batchUpdate(spreadsheetId=UserList.SPREADSHEET_ID, body={"requests" :UserList.request_list}).execute()
        [user.set_metadataId(reply['createDeveloperMetadata']['developerMetadata']['metadataId']) for user,reply in zip(User.all_users, response['replies'])]
        UserList.request_list = []

class User:
    all_users = UserList()
    
    def __init__(self, userType:str = None, sheetID:int = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        if userType == "Admin":
            AdminUser(userType, sheetID, df)
        elif userType == "Wholesale":
            WholesaleUser(userType, sheetID, df)
        else:
            logging.info("Invalid type of user, check User Class")

    def set_metadataId(self, metadataId:int) -> None:
        self.metadataId = metadataId

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
            
        self.all_users.sheet.values().batchUpdateByDataFilter(spreadsheetId=self.all_users.SAMPLE_SPREADSHEET_ID, body=batch_datafilter_update).execute()
        
    def refresh(self) -> None:
        batch_request_get = {

            'data_filters': [{'developerMetadataLookup': {'metadataId': self.metadataId
                                                          }}]  # TODO: Update placeholder value.

        }
        
        response =  User.all_users.sheet.values().batchGetByDataFilter(spreadsheetId= User.all_users.SAMPLE_SPREADSHEET_ID, body = batch_request_get).execute()
        self.mmsUserID,self.firstName,self.lastName,self.telegramUserID,self.access = response['valueRanges'][0]['valueRange']['values'][0][0:5]
        


class AdminUser(User):
    def __init__(self, userType:str = None, sheetID:int = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
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
        
        try:
            self.sheetID = sheetID
        except:
            self.sheetID = None
            
        self.metadataId = None
        
        if sheetID != None:
            User.all_users.request_list += [{"createDeveloperMetadata": \
                                                 {"developerMetadata": {
                                                     "metadataKey": "sheetID"+f"{df[0]+1}",
                                                     "location" : {"dimensionRange":
                                                                   {"sheetId": sheetID,
                                                                    "dimension":"ROWS",
                                                                    "startIndex": df[0]+1,
                                                                    "endIndex": df[0]+2}
                                                                   },
                                                     "visibility": "DOCUMENT"}
                                                         }}]
        
        User.all_users.append(self)
        
        logging.info(f"Created {type(self)} user {self.firstName}")

class WholesaleUser(User):
    def __init__(self, userType:str = None, sheetID:int = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
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
        
        try:
            self.sheetID = sheetID
        except:
            self.sheetID = None
        
        try:
            pass
            #self.business:Business = BusinessList.search(df[1]['Assigned Business'],"MMS Business ID")[0]
        except:
            pass
            #self.business:Business = None
            
        self.metadataId = None
            
        if sheetID != None:
            User.all_users.request_list += [{"createDeveloperMetadata": \
                                                 {"developerMetadata": {
                                                     "metadataKey": "sheetID"+f"{df[0]+1}",
                                                     "location" : {"dimensionRange":
                                                                   {"sheetId": sheetID,
                                                                    "dimension":"ROWS",
                                                                    "startIndex": df[0]+1,
                                                                    "endIndex": df[0]+2}
                                                                   },
                                                     "visibility": "DOCUMENT"}
                                                         }}]
                
        User.all_users.append(self)
        
        logging.info(f"Created {type(self)} user {self.firstName}")