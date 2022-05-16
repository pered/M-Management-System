from typing import Optional, Tuple, Dict, List
from .ext import Sheets
import logging
import json
from pandas import DataFrame, Series

class BusinessList(Sheets, list['Business']): 

    SPREADSHEET_ID = "104m9PVDzrz4yK-AD0u5ai8_aMTmcUKYuz9prZHq0CV4"
    sheet_info = [{"Range": "Wholesale",
                    "sheetID": 0},
                  {"Range": "Internal",
                    "sheetID": 1788602125}]
    
    request_list:List = []
    
    def __init__(self):
        super().__init__(write_sheet=True)
        #Delete all previous metadata from users sheets, reference to Wholesale and Admin sections
        logging.info("Initializing businesses from business sheet")
        delete_all = {"requests" : [
            {"deleteDeveloperMetadata":{"dataFilter": {\
            "developerMetadataLookup": {"metadataLocation": {"sheetId":sheets["sheetID"]}}}}} for sheets in self.sheet_info 
            ]}
        self.sheet.batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=delete_all).execute()
        logging.info("Initialised businesses from business sheet")
        
    def load(self):
        if BusinessList.__len__ != 0:
            BusinessList.clear(self)
            logging.info("Reloaded business list")
        
        self.results = Sheets.load(self)
        
        #Create a list of objects with products in them
        [[Business(BusinessList.sheet_info[index]['Range'], BusinessList.sheet_info[index]['sheetID'], sf_business)
          for sf_business in df_business.iterrows()] 
             for index, df_business in [(self.results['valueRanges'].index(businessRange),DataFrame(businessRange['values'][1:], columns = businessRange['values'][0])) 
                                       for businessRange in self.results['valueRanges']]]
        
        response = self.sheet.batchUpdate(spreadsheetId=BusinessList.SPREADSHEET_ID, body={"requests" :BusinessList.request_list}).execute()
        [business.set_metadataId(reply['createDeveloperMetadata']['developerMetadata']['metadataId']) for business,reply in zip(Business.all_businesses, response['replies'])]
        BusinessList.request_list = []
        
    def refresh(self) -> None:
        #Add batch search, current code is not good
        # [business.refresh() for business in self]
        # logging.info("Refreshed data for all businesses")
        pass
        
    
    def search(self, businessType = None, mmsbusinessId = None, businessName:str = None, business_toSearch:List = None) -> List:
        '''This function returns objects that match the value with the given attribute'''
        if business_toSearch == None:
            business_toSearch = Business.all_businesses
        
        try:
            search_results = list(filter(lambda z: (businessType == None or type(z).__name__ == businessType), business_toSearch))
            search_results = list(filter(lambda z: (mmsbusinessId == None or z.mmsbusinessId == mmsbusinessId), search_results))
            search_results = list(filter(lambda z: (businessName == None or z.businessName == businessName), search_results))
            return search_results
        except:
            raise ValueError("Tried to seach for an invalid weight in products")
            return []

class Business:
    all_businesses = BusinessList()
    
    def __init__(self, businessType:str = None, sheetID:int = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        if businessType == "Wholesale":
            WholesaleBusiness(businessType, sheetID, df)
        elif businessType == "Internal":
            InternalBusiness(businessType, sheetID, df)
        else:
            logging.info("Invalid type of bsiness, check Business Class")

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
    
        
    def refresh(self) -> None:
        Business.refresh(self)
        self.address,self.pluscode = self.response['valueRanges'][0]['valueRange']['values'][0][3:5]
    
    def save(self) -> None:
        batch_datafilter_update = {"valueInputOption": 'USER_ENTERED',
                                    "data": [{"dataFilter": {'developerMetadataLookup': 
                                                            {'metadataId': self.metadataId
                                                            }},
                                    "majorDimension": 'ROWS',
                                    "values": [[self.mmsbusinessId, self.telegramChatId, self.businessName, self.address, self.pluscode]
                                                ]}]}
            
        Business.all_businesses.sheet.values().batchUpdateByDataFilter(spreadsheetId=Business.all_businesses.SPREADSHEET_ID, body=batch_datafilter_update).execute()


class WholesaleBusiness(Business):
    def __init__(self, userType:str = None, sheetID:int = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        try:
            self.mmsbusinessId = df[1]['MMS Business ID']
        except:
            self.mmsbusinessId = None
            
        try:
            self.telegramChatId:str = df[1]['Telegram Chat ID']
        except:
            self.telegramChatId:str = None
        
        try:
            self.businessName = df[1]['Business Name']
        except:
            self.businessName = None
        try:
            self.address = df[1]['Address']
        except:
            self.address = None
        try:
            self.pluscode = df[1]['Plus Code']
        except:
            self.pluscode = None
                
            
        self.metadataId = None
        
        if sheetID != None:
            Business.all_businesses.request_list += [{"createDeveloperMetadata": \
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
        
        Business.all_businesses.append(self)
        
        logging.info(f"Created {type(self)} user {self.businessName}")

class InternalBusiness(Business):
    def __init__(self, userType:str = None, sheetID:int = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        try:
            self.mmsbusinessId = df[1]['MMS Business ID']
        except:
            self.mmsbusinessId = None
            
        try:
            self.telegramChatId:str = df[1]['Telegram Chat ID']
        except:
            self.telegramChatId:str = None
        
        try:
            self.businessName = df[1]['Business Name']
        except:
            self.businessName = None
        try:
            self.address = df[1]['Address']
        except:
            self.address = None
        try:
            self.pluscode = df[1]['Plus Code']
        except:
            self.pluscode = None
                
        
        self.metadataId = None
            
        if sheetID != None:
            Business.all_businesses.request_list += [{"createDeveloperMetadata": \
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
                
        Business.all_businesses.append(self)
        
        logging.info(f"Created {type(self)} user {self.businessName}")
        
    
            