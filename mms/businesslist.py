from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build

import logging

from typing import List
from pandas import DataFrame
from .businesses import Business

class BusinessList: 
    businessList:List = []
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SAMPLE_SPREADSHEET_ID = "104m9PVDzrz4yK-AD0u5ai8_aMTmcUKYuz9prZHq0CV4"
    PAGE1_SHEETID = 0
    
    #Variables refering to methods for cloud sheets manipulation
    creds = service_account.Credentials.from_service_account_file(\
            'maximal-copilot-343018-f149332a7912.json',scopes=SCOPES)
    sheet = build('sheets','v4', credentials=creds).spreadsheets()   
   
    #Lists used for batch executions of developer metadata
    request_list:List = []
        
    def __init__(self) -> None:
        logging.info("Initializing settings from settings sheet")
        
        logging.info("Initialised settings from settings sheet")
        
    @classmethod
    def load(cls):
        results = BusinessList.sheet.values().batchGet(\
                            spreadsheetId = BusinessList.SAMPLE_SPREADSHEET_ID,\
                            ranges=['Page1']).execute()
            
        #Creating DataFrames for creation of user objects
        business_df = DataFrame(results['valueRanges'][0]['values'][1:], columns = results['valueRanges'][0]['values'][0]) 
        
        #Creation of userList with User objects
        cls.businessList += [Business(x, BusinessList.PAGE1_SHEETID) for x in business_df.iterrows()]



        response = BusinessList.sheet.batchUpdate(spreadsheetId=BusinessList.SAMPLE_SPREADSHEET_ID, body={"requests" :BusinessList.request_list}).execute()
        [business.set_metadataId(reply['createDeveloperMetadata']['developerMetadata']['metadataId']) for business,reply in zip(BusinessList.businessList, response['replies'])]
        BusinessList.request_list = []

        logging.info("Business list loading complete")
        
    @classmethod
    def reload(cls):
        results = BusinessList.sheet.values().batchGet(\
                            spreadsheetId = BusinessList.SAMPLE_SPREADSHEET_ID,\
                            ranges=[BusinessList.PAGE1_SHEETID]).execute()
            
        #Creating DataFrames for creation of user objects
        business_df = DataFrame(results['valueRanges'][0]['values'][1:], columns = results['valueRanges'][0]['values'][0]) 
        
        
        #Creation of userList with User objects
        cls.businessList += [Business(x) for x in business_df.iterrows()]

        logging.info("Business list loading complete")
        
    @classmethod
    def search(cls, value, attribute:str, business_toSearch:List = businessList) -> List:
            '''This function searches if value is in any users of the userlist, given is a value and an attribute to search.\
                Values can be any type, whether int or str, whilst attribute must be of any attribute type found in users'''

            if attribute  == "MMS Business ID":
                try:
                    return [x for x in business_toSearch if x.mmsbusinessId == value]
                except:
                    logging.info("Business is not in database")
                    return []
            elif attribute  == "Telegram Chat ID":
                try:
                    return [x for x in business_toSearch if x.telegramChatId == value]
                except:
                    logging.info("No businesses to register")
                    return []
            elif attribute  == "Business Name":
                try:
                    return [x for x in business_toSearch if x.businessName == value]
                except:
                    logging.info("No businesses matches")
                    return []
                