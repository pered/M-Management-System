from typing import Optional, Tuple, Dict, List
from .ext import Sheets
import logging
import json
from pandas import DataFrame, Series
from mms.business import Business

class UserList(Sheets, list['User']): 

    SPREADSHEET_ID = "10bzoC_M0GOyEB8CH5zY9EXE7tGtxnC8vwJO3tTBDkyA"
    sheet_info = [{"Range": "Wholesale",
                    "sheetID": 0},
                  {"Range": "Internal",
                   "sheetID": 1901208172},
                  {"Range": "Admin",
                    "sheetID": 1929008158}]
    
    request_list:List = []
    batch_datafilter:List = []
    batch_request:List = []
    
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
        if User.all_users.__len__() != 0:
            User.all_users.clear()
            logging.info("Reloaded user list")
        
        self.results = Sheets.load(self)
        
        #Create a list of objects with users in them
        [[User(UserList.sheet_info[index]['Range'], UserList.sheet_info[index]['sheetID'], sf_user)
          for sf_user in df_user.iterrows()] 
             for index, df_user in [(self.results['valueRanges'].index(userRange),DataFrame(userRange['values'][1:], columns = userRange['values'][0])) 
                                       for userRange in self.results['valueRanges']]]
        
        ### Assign metadataID to users
        response = self.sheet.batchUpdate(spreadsheetId=UserList.SPREADSHEET_ID, body={"requests" :UserList.request_list}).execute()
        [user.set_metadataId(reply['createDeveloperMetadata']['developerMetadata']['metadataId']) for user,reply in zip(User.all_users, response['replies'])]
        UserList.request_list.clear()
    
    def save(self) -> None:
        #Create datafilters for all the users
        [user.create_datafilter() for user in self]
        
        #Make a dictionary for google api
        batch_datafilter_update = {"valueInputOption": 'USER_ENTERED',
                                    "data": UserList.batch_datafilter}
        
        #Send the request and clear the datafilter
        User.all_users.sheet.values().batchUpdateByDataFilter(spreadsheetId=User.all_users.SPREADSHEET_ID, body=batch_datafilter_update).execute()
        User.all_users.batch_datafilter.clear()

    def search(self, userType = None, mmsUserId = None, telegramUserID:str = None, access:str = None, user_toSearch:List = None) -> List:
        '''This function returns objects that match the value with the given attribute'''
        if user_toSearch == None:
            user_toSearch = User.all_users
        
        try:
            search_results = list(filter(lambda z: (userType == None or type(z).__name__ == userType), user_toSearch))
            search_results = list(filter(lambda z: (access == None or z.access == access), search_results))
            search_results = list(filter(lambda z: (mmsUserId == None or z.mmsUserId == mmsUserId), search_results))
            search_results = list(filter(lambda z: (telegramUserID == None or z.telegramUserID == telegramUserID), search_results))
            return search_results
        except:
            raise ValueError("Invalid input for search method in users")
            return []
    
    def print(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        

class User:
    all_users = UserList()
    
    def __init__(self, userType:str = None, sheetID:int = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        if userType == "Admin":
            AdminUser(userType, sheetID, df)
        elif userType == "Wholesale":
            WholesaleUser(userType, sheetID, df)
        elif userType == "Internal":
            InternalUser(userType, sheetID, df)
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
    
    def create_datafilter(self) -> None:
        User.all_users.batch_datafilter += [{"dataFilter": {'developerMetadataLookup': 
                                                            {'metadataId': self.metadataId
                                                            }},
                                    "majorDimension": 'ROWS',
                                    "values": [[self.mmsUserId, self.firstName, self.lastName, self.telegramUserID, self.access]
                                                ]}]
        
    def save(self)-> None:
        self.create_datafilter()
        batch_datafilter_update = {"valueInputOption": 'USER_ENTERED',
                                    "data": User.all_users.batch_datafilter}
        
        User.all_users.sheet.values().batchUpdateByDataFilter(spreadsheetId=User.all_users.SPREADSHEET_ID, body=batch_datafilter_update).execute()
        User.all_users.batch_datafilter.clear()
        
    def create_refresh(self) -> None:
        User.all_users.batch_request += [{'developerMetadataLookup': {'metadataId': self.metadataId
                                                      }}]
        
        


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
            self.mmsUserId:str = df[1]['MMS UserID']
        except:
            self.mmsUserId:str = str()
            
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
        
    def refresh(self) -> None:
        self.create_refresh()
        batch_request_get = {

            'data_filters': User.all_users.batch_request  # TODO: Update placeholder value.

        }
        
        response =  User.all_users.sheet.values().batchGetByDataFilter(spreadsheetId= User.all_users.SPREADSHEET_ID, body = batch_request_get).execute()
        self.mmsUserId,self.firstName,self.lastName,self.telegramUserID,self.access = response['valueRanges'][0]['valueRange']['values'][0][0:5]
        User.all_users.batch_request.clear()

class NonAdminUser(User):
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
            self.mmsUserId:str = df[1]['MMS UserID']
        except:
            self.mmsUserId:str = str()
            
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
            self.business:Business = Business.all_businesses.search(mmsbusinessId=df[1]['Assigned Business'])[0]
        except:
            self.business:Business = None
            
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
        
        def refresh(self) -> None:
            self.create_refresh()
            batch_request_get = {

                'data_filters': User.all_users.batch_request  # TODO: Update placeholder value.

            }
            
            response =  User.all_users.sheet.values().batchGetByDataFilter(spreadsheetId= User.all_users.SPREADSHEET_ID, body = batch_request_get).execute()
            self.mmsUserId,self.firstName,self.lastName,self.telegramUserID,self.access = response['valueRanges'][0]['valueRange']['values'][0][0:5]
            User.all_users.batch_request.clear()

class InternalUser(NonAdminUser):
    def __init__(self, userType:str = None, sheetID:int = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        super().__init__(userType, sheetID, df)

class WholesaleUser(NonAdminUser):
    def __init__(self, userType:str = None, sheetID:int = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        super().__init__(userType, sheetID, df)