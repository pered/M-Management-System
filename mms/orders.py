from typing import Optional,List
import logging 

from .ext import Sheets

class OrderList(Sheets, list['Order']):
    
    SPREADSHEET_ID = "1OfaG4VCbM834Fe4TdtIjQF7jcETBNt5dKNbzEDrftLk"
    sheet_info = [{"Range": "April 2022",
                    "sheetID": 0}]
    
    def __init__(self):
        super(Sheets, self).__init__(write=True)
    
    def load(self):
        if OrderList.__len__ != 0:
            OrderList.clear(self)
            logging.info("Reloaded product list")
        
        #From sheets obtain results from sheet
        self.results = Sheets.load(self)
        
        

class Order:
    all_orders = OrderList()
    
    def __init__(self):
        pass
    


