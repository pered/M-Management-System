from __future__ import print_function, annotations
from google.oauth2 import service_account
from googleapiclient.discovery import build

import logging
from typing import List,Tuple,Dict, overload
from pandas import Series, DataFrame



class Sheets:
    sheet_info:List[Dict] = [{}]
    
    def __init__(self, write:bool = False):
        if write == True:
            self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            self.creds = service_account.Credentials.from_service_account_file(\
                    'maximal-copilot-343018-f149332a7912.json',scopes=self.SCOPES)
                
            self.sheet = build('sheets','v4', credentials=self.creds).spreadsheets()   
            
            delete_all = {"requests" : [{"deleteDeveloperMetadata":{"dataFilter": {\
            "developerMetadataLookup": {"metadataLocation": {"sheetId":product["sheetID"]}}}}} for product in self.sheet_info
                ]}
           
            self.sheet.batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=delete_all).execute()
        else:
            self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            self.creds = service_account.Credentials.from_service_account_file(\
                    'maximal-copilot-343018-f149332a7912.json',scopes=self.SCOPES)
                
            self.sheet = build('sheets','v4', credentials=self.creds).spreadsheets()   
        
  
class ProductList(Sheets, list['Product']):
    SPREADSHEET_ID = "1mCJyUwHad0RBj14d8pvYC1EaCd4mHNwzkDKiUYTcLy4"
    sheet_info = [{"Range": "Coffee",
                    "sheetID": 0},
                  {"Range": "Sugar",
                    "sheetID": 1980308451},
                  {"Range" : "Beverages", 
                    "sheetID": 366404389}]

    def __init__(self, write:bool = False):
          Sheets.__init__(self)
          logging.info("Initialized product list")
    
    def load(self):
        self.results = self.sheet.values().batchGet(spreadsheetId = self.SPREADSHEET_ID,\
                            ranges=[product["Range"] for product in self.sheet_info]).execute()
        
        #dfRanges = [DataFrame(productRange['values'][1:], columns = productRange['values'][0]) for productRange in test.all_products.results['valueRanges']]
    
        [[Product(ProductList.sheet_info[index]['Range'],sf_product)
          for sf_product in df_product.iterrows()] 
             for index, df_product in [(self.results['valueRanges'].index(productRange),DataFrame(productRange['values'][1:], columns = productRange['values'][0])) 
                for productRange in self.results['valueRanges']]]
    
class Product:
    all_products = ProductList()
    
    def __init__(self,productType:str = None,df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        logging.info("Initializing products")
        if productType == 'Coffee':
            self.productId:str = df[1]['Product ID']
            self.displayName:str = df[1]['Display Name']
            self.farmName:str = df[1]['Farm']
            self.origin:str = df[1]['Origin']
            self.grinds:List = df[1]['Grinds']
            self.weights:List = df[1]['Weight']
            self.price:List = df[1]['Price']
        elif productType == 'Sugar':
            self.productId:str = df[1]['Product ID']
        elif productType == 'Beverages':
            self.productId:str = df[1]['Product ID']
            
        Product.all_products.append(self)
        
        
