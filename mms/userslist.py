from __future__ import print_function
import os.path
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
    ADMIN_SAMPLE_RANGE_NAME = 'Admin!A1:E'
    WHOLESALE_SAMPLE_RANGE_NAME = 'Wholesale!A1:F'
    
    creds = service_account.Credentials.from_service_account_file(\
            'maximal-copilot-343018-f149332a7912.json',scopes=SCOPES)
    
    adminSheet = build('sheets','v4', credentials=creds).spreadsheets()
    wholesaleSheet = build('sheets','v4', credentials=creds).spreadsheets()    
        
    def __init__(self) -> None:
        pass
    
    @classmethod
    def load(cls) -> None:
        adminResults = UserList.adminSheet.values().get(spreadsheetId=\
                            UserList.SAMPLE_SPREADSHEET_ID, range=\
                                UserList.ADMIN_SAMPLE_RANGE_NAME).execute()
            
        wholesaleResults = UserList.wholesaleSheet.values().get(spreadsheetId=\
                            UserList.SAMPLE_SPREADSHEET_ID, range=\
                                UserList.WHOLESALE_SAMPLE_RANGE_NAME).execute() 
            
        #Creating DataFrames for creation of user objects
    
        admin_df = DataFrame(adminResults['values'][1:], columns = adminResults['values'][0])
        wholesale_df = DataFrame(wholesaleResults['values'][1:], columns = wholesaleResults['values'][0])
        
        ##Check this ##
        cls.userList += [Admin(x[1]) for x in admin_df.iterrows()]
        cls.userList += [WholesaleUser(x[1]) for x in wholesale_df.iterrows()]
    
    @classmethod
    def reload(cls) -> None:
        cls.userList = []
        
        adminResults = UserList.adminSheet.values().get(spreadsheetId=\
                            UserList.SAMPLE_SPREADSHEET_ID, range=\
                                UserList.ADMIN_SAMPLE_RANGE_NAME).execute()
            
        wholesaleResults = UserList.wholesaleSheet.values().get(spreadsheetId=\
                            UserList.SAMPLE_SPREADSHEET_ID, range=\
                                UserList.WHOLESALE_SAMPLE_RANGE_NAME).execute() 
            
        #Creating DataFrames for creation of user objects
    
        admin_df = DataFrame(adminResults['values'][1:], columns = adminResults['values'][0])
        wholesale_df = DataFrame(wholesaleResults['values'][1:], columns = wholesaleResults['values'][0])
        
        ##Check this ##
        cls.userList += [Admin(x[1]) for x in admin_df.iterrows()]
        cls.userList += [WholesaleUser(x[1]) for x in wholesale_df.iterrows()] 
    
    @classmethod
    def search(cls, value, attribute:str) -> List:
        '''This function searches if value is in any users of the userlist, given is a value and an attribute to search.\
            Values can be any type, whether int or str, whilst attribute must be of any attribute type found in users'''
        if attribute  == "Telegram UserID":
            try:
                return [x for x in cls.userList if x.telegramUserID == value]
            except:
                logging.info("User is not in database")
                return []
        elif attribute  == "Access":
            try:
                return [x for x in cls.userList if x.access == value]
            except:
                logging.info("No businesses to register")
                return []
        elif attribute  == "Business Name":
            try:
                return [x for x in cls.userList if x.businessName == value]
            except:
                logging.info("No businesses matches")
                return []
            
    @classmethod
    def assign_User(cls, user_toAssign:Union[WholesaleUser, Admin]):
        pass