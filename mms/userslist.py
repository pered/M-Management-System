from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build

import logging

from typing import List, Optional, Tuple, Union
from pandas import DataFrame
from .users import Admin, WholesaleUser, User

class UserList: 
    userList: List[User] = []
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SAMPLE_SPREADSHEET_ID = "10bzoC_M0GOyEB8CH5zY9EXE7tGtxnC8vwJO3tTBDkyA"
    
    ADMIN_SAMPLE_RANGE_NAME = 'Admin'
    WHOLESALE_SAMPLE_RANGE_NAME = 'Wholesale'
    
    WHOLESALE_SHEETID = 0
    ADMIN_SHEETID = 1929008158
    
    #Lists used for batch executions of developer metadata
    request_list:List = []
    
    
    #Variables refering to methods for cloud sheets manipulation
    creds = service_account.Credentials.from_service_account_file(\
            'maximal-copilot-343018-f149332a7912.json',scopes=SCOPES)
    sheet = build('sheets','v4', credentials=creds).spreadsheets()   
        
    def __init__(self) -> None:
        #Delete all previous metadata from users sheets, reference to Wholesale and Admin sections
        logging.info("Initializing users from user sheet")
        delete_all = {"requests" : [
            {"deleteDeveloperMetadata":{"dataFilter": {\
            "developerMetadataLookup": {"metadataLocation": {"sheetId":UserList.WHOLESALE_SHEETID}}}}},
            {"deleteDeveloperMetadata":{"dataFilter": {\
           "developerMetadataLookup": {"metadataLocation": {"sheetId":UserList.ADMIN_SHEETID}}}}}
            ]}
       
        UserList.sheet.batchUpdate(spreadsheetId=UserList.SAMPLE_SPREADSHEET_ID, body=delete_all).execute()
        logging.info("Initialised users from user sheet")
    #Cloud server methods
    
    @classmethod
    def search(cls, value, attribute:str, userList_toSearch:List = None) -> List:
        '''This function searches if value is in any users of the userlist, given is a value and an attribute to search.\
            Values can be any type, whether int or str, whilst attribute must be of any attribute type found in users'''
        if userList_toSearch == None:
            userList_toSearch = UserList.userList
        
        if attribute  == "Telegram UserID":
            print([test.telegramUserID for test in UserList.userList])
            print([test.telegramUserID for test in userList_toSearch])
            try:
                return [x for x in userList_toSearch if x.telegramUserID == str(value)]
            except:
                logging.info("User is not in database")
                return []
        elif attribute  == "Access":
            try:
                return [x for x in userList_toSearch if x.access == value]
            except:
                logging.info(f"No users with specified access level {value}")
                return []
        elif attribute  == "Business Name":
            try:
                return [x for x in userList_toSearch if x.business.businessName == value]
            except:
                logging.info("No businesses matches")
                return []
    
    @classmethod
    def load(cls) -> None:
        #Obtain the values of cloud sheet
        results = UserList.sheet.values().batchGet(\
                            spreadsheetId = UserList.SAMPLE_SPREADSHEET_ID,\
                            ranges=[UserList.WHOLESALE_SAMPLE_RANGE_NAME, UserList.ADMIN_SAMPLE_RANGE_NAME]).execute()
            
        #Creating DataFrames for creation of user objects
        wholesale_df = DataFrame(results['valueRanges'][0]['values'][1:], columns = results['valueRanges'][0]['values'][0])
        admin_df = DataFrame(results['valueRanges'][1]['values'][1:], columns = results['valueRanges'][1]['values'][0])
        
        
        
        #Creation of userList with User objects
        UserList.userList += [WholesaleUser(x, UserList.WHOLESALE_SHEETID) for x in wholesale_df.iterrows()]
        UserList.userList += [Admin(x, UserList.ADMIN_SHEETID) for x in admin_df.iterrows()]
       
    
        response = UserList.sheet.batchUpdate(spreadsheetId=UserList.SAMPLE_SPREADSHEET_ID, body={"requests" :UserList.request_list}).execute()
        [user.set_metadataId(reply['createDeveloperMetadata']['developerMetadata']['metadataId']) for user,reply in zip(UserList.userList, response['replies'])]
        UserList.request_list = []
        logging.info("User list loading complete")
    
    @classmethod
    def reload_all(cls) -> None:
        #Delete all previous metadata from users sheets, reference to Wholesale and Admin sections
        delete_all = {"requests" : [
            {"deleteDeveloperMetadata":{"dataFilter": {\
            "developerMetadataLookup": {"metadataLocation": {"sheetId":UserList.WHOLESALE_SHEETID}}}}},
            {"deleteDeveloperMetadata":{"dataFilter": {\
           "developerMetadataLookup": {"metadataLocation": {"sheetId":UserList.ADMIN_SHEETID}}}}}
            ]}
        UserList.sheet.batchUpdate(spreadsheetId=UserList.SAMPLE_SPREADSHEET_ID, body=delete_all).execute()
        
        #Delete all User objects
        UserList.userList = []
        
        results = UserList.sheet.values().batchGet(\
                            spreadsheetId = UserList.SAMPLE_SPREADSHEET_ID,\
                            ranges=[UserList.WHOLESALE_SAMPLE_RANGE_NAME, UserList.ADMIN_SAMPLE_RANGE_NAME]).execute()
            
        #Creating DataFrames for creation of user objects
        wholesale_df = DataFrame(results['valueRanges'][0]['values'][1:], columns = results['valueRanges'][0]['values'][0])
        admin_df = DataFrame(results['valueRanges'][1]['values'][1:], columns = results['valueRanges'][1]['values'][0])
        
        
        
        #Creation of userList with User objects
        UserList.userList += [WholesaleUser(x, UserList.WHOLESALE_SHEETID) for x in wholesale_df.iterrows()]
        UserList.userList += [Admin(x, UserList.ADMIN_SHEETID) for x in admin_df.iterrows()]
        
        response = UserList.sheet.batchUpdate(spreadsheetId=UserList.SAMPLE_SPREADSHEET_ID, body={"requests" :UserList.request_list}).execute()
        [user.set_metadataId(reply['createDeveloperMetadata']['developerMetadata']['metadataId']) for user,reply in zip(UserList.userList, response['replies'])]
        UserList.request_list = []
        
        logging.info("User list reload complete")
    #Complex class methods
    
    
            