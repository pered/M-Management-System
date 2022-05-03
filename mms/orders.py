from typing import Optional,List
import logging 
from pandas import DataFrame

#from .businesses import Business
#from .users import User
from .products import Product
from .ext import Sheets

class OrderList(Sheets, list['Order']):
    
    SPREADSHEET_ID = "1OfaG4VCbM834Fe4TdtIjQF7jcETBNt5dKNbzEDrftLk"
    sheet_info = [{"Range": "04/2022!A1:S",
                    "sheetID": 0}]
    
    def __init__(self):
        super().__init__(write_sheet=True)
    
    def load(self):
        if OrderList.__len__ != 0:
            OrderList.clear(self)
            logging.info("Reloaded product list")
        
        #From sheets obtain results from sheet
        self.results = Sheets.load(self)
        
        df = DataFrame(self.results['valueRanges'][0]['values'][1:], columns = self.results['valueRanges'][0]['values'][0])
        
        

class Order:
    all_orders = OrderList()
    
    def __init__(self):
        pass
    
class OrderItem:
    
    def __init__(self):
        self.orderNo = None
        self.orderDate = None
        self.orderId = None
        self.user:User = None
        self.business:Business = None
        self.product:Product = None
    


