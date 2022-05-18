from typing import Optional,List
import logging 
from pandas import DataFrame

from .businesses import Business
from .users import User
from .products import Product
from .ext import Sheets
from .orders import Order


class ReccuringOrderList(Sheets, list['RecurringOrder']):
    
    SPREADSHEET_ID = "1OfaG4VCbM834Fe4TdtIjQF7jcETBNt5dKNbzEDrftLk"
    sheet_info = [{"Range": "Recurring",
                    "sheetID": 0},
                  {"Range": "05/2022!A1:S",
                   "sheetID": 673559976}]
    
    request_list:List = []
    
    def __init__(self):
        super().__init__(write_sheet=True)
        #Delete all previous metadata from users sheets, reference to Wholesale and Admin sections
        logging.info("Initializing users from user sheet")
        delete_all = {"requests" : [
            {"deleteDeveloperMetadata":{"dataFilter": {\
            "developerMetadataLookup": {"metadataLocation": {"sheetId":sheets["sheetID"]}}}}} for sheets in self.sheet_info 
            ]}
        self.sheet.batchUpdate(spreadsheetId=ReccuringOrderList.SPREADSHEET_ID, body=delete_all).execute()
        logging.info("Initialised recurring orders from recurring order sheet")
    
    def load(self):
        if ReccuringOrderList.__len__ != 0:
            ReccuringOrderList.clear(self)
            logging.info("Reloaded product list")
        
        self.results = Sheets.load(self)
        
        #Create a list of objects with users in them
        [[RecurringOrder(ReccuringOrderList.sheet_info[index]['Range'], ReccuringOrderList.sheet_info[index]['sheetID'], sf_rorder)
          for sf_rorder in df_rorder.iterrows()] 
             for index, df_rorder in [(self.results['valueRanges'].index(rorderRange),DataFrame(rorderRange['values'][1:], columns = rorderRange['values'][0])) 
                                       for rorderRange in self.results['valueRanges']]]
        
        ### Assign metadataID to users
        response = self.sheet.batchUpdate(spreadsheetId=ReccuringOrderList.SPREADSHEET_ID, body={"requests" :ReccuringOrderList.request_list}).execute()
        [rorder.set_metadataId(reply['createDeveloperMetadata']['developerMetadata']['metadataId']) for rorder,reply in zip(Order.all_orders, response['replies'])]
        ReccuringOrderList.request_list.clear()

class RecurringOrder(list["RecurringOrderItem"]):
    all_recurringorders = ReccuringOrderList()
    def __init__(self)  -> None:
        pass
    
    
class RecurringOrderItem:
    def __init__(self):
        pass    