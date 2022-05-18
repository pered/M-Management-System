from typing import Optional,List
import logging 
from pandas import DataFrame

from .businesses import Business
from .users import User
from .products import Product
from .ext import Sheets

class OrderList(Sheets, list['Order']):
    
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
        self.sheet.batchUpdate(spreadsheetId=OrderList.SPREADSHEET_ID, body=delete_all).execute()
        logging.info("Initialised orders from order sheet")
    
    def load(self):
        if OrderList.__len__ != 0:
            OrderList.clear(self)
            logging.info("Reloaded product list")
        
        self.results = Sheets.load(self)
        
        #Create a list of objects with users in them
        [[Order(OrderList.sheet_info[index]['Range'], OrderList.sheet_info[index]['sheetID'], sf_order)
          for sf_order in df_order.iterrows()] 
             for index, df_order in [(self.results['valueRanges'].index(orderRange),DataFrame(orderRange['values'][1:], columns = orderRange['values'][0])) 
                                       for orderRange in self.results['valueRanges']]]
        
        ### Assign metadataID to users
        response = self.sheet.batchUpdate(spreadsheetId=OrderList.SPREADSHEET_ID, body={"requests" :OrderList.request_list}).execute()
        [order.set_metadataId(reply['createDeveloperMetadata']['developerMetadata']['metadataId']) for order,reply in zip(Order.all_orders, response['replies'])]
        OrderList.request_list.clear()
        

class Order(list("OrderItem")):
    all_orders = OrderList()
    def __init__(self):
        self.orderNo = None
        self.orderDate = None
        self.orderId = None
        self.user:User = None
        self.business:Business = None
        self.deliveryDate = None
        self.returnedPackages:str = None
    
    def set_metadataId(self, metadataId:int) -> None:
        self.metadataId = metadataId

    @property
    def metadataId(self) -> int:
        return self._metadataId
        
    @metadataId.setter
    def metadataId(self, metadataId:int) -> None:
        self._metadataId = metadataId
    

class OrderItem:
    
    def __init__(self):
        self.product:Product = None
        self.quantity = None
        self.deliveryNote:bool = False
        self.lotNo = None
        self.packaging:str = None
        self.packaged:bool = None

        
    



    
