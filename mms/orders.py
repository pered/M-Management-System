from typing import Optional,List, Tuple
import logging 
from pandas import DataFrame, Series

from .business import Business
from .users import User
from .product import Product
from .ext import Sheets

class OrderList(Sheets, list['Order']):
    
    SPREADSHEET_ID = "1OfaG4VCbM834Fe4TdtIjQF7jcETBNt5dKNbzEDrftLk"
    sheet_info = [{"Range": "Recurring",
                    "sheetID": 0},
                  {"Range": "05/2022",
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
        if Order.all_orders.__len__() != 0:
            Order.all_orders.clear()
            logging.info("Reloaded order list")
        
        self.results = Sheets.load(self)
        
        #Create a list of objects with users in them
        [[OrderItem(OrderList.sheet_info[index]['sheetID'], sf_order)
          for sf_order in df_order.iterrows()] 
             for index, df_order in [(self.results['valueRanges'].index(orderRange),DataFrame(orderRange['values'][1:], columns = orderRange['values'][0])) 
                                       for orderRange in self.results['valueRanges'][1:]]]
        
        ### Assign metadataID to users
        response = self.sheet.batchUpdate(spreadsheetId=OrderList.SPREADSHEET_ID, body={"requests" :OrderList.request_list}).execute()
        [order.set_metadataId(reply['createDeveloperMetadata']['developerMetadata']['metadataId']) for order,reply in zip([orderitem for order in Order.all_orders for orderitem in order], response['replies'])]
        OrderList.request_list.clear()
        logging.info("Finished loading all orders")

    def search(self, orderType = None, orderId = None, order_toSearch:List = None) -> List:
        '''This function returns objects that match the value with the given attribute'''
        if order_toSearch == None:
            order_toSearch = Order.all_orders
        
        try:
            search_results = list(filter(lambda z: (orderType == None or type(z).__name__ == orderType), order_toSearch))
            search_results = list(filter(lambda z: (orderId == None or z.orderId == orderId), search_results))
            return search_results
        except:
            raise ValueError("Tried to seach for an invalid order in orders")
            return []    

class Order(list['OrderItem']):
    all_orders = OrderList()
    def __init__(self, orderItem:"OrderItem" = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        order_match = Order.all_orders.search(orderId=df[1]["Order ID"])
        if order_match != []:
            try:
                if len(order_match) == 1:
                    order_match[0].append(orderItem)
                else:
                    raise ValueError("Too many order matches")
            except:
                pass
        else:
            try:
                self.orderNo = df[1]["Order No."]
            except:
                self.orderNo = None
            try:
                self.orderDate = df[1]["Order Date"]
            except:
                self.orderDate = None
            try:
                self.orderId = df[1]["Order ID"]
            except:
                self.orderId = None
            try:   
                self.user:User = User.all_users.search(mmsUserId=df[1]["Order Creator ID"])
            except:
                self.user:User = None
            try:
                self.business = Business.all_businesses.search(mmsbusinessId =  df[1]["Business ID"], businessName = df[1]["Business Name"])
            except:  
                self.business:Business = None
            try:
                self.append(orderItem)
            except:
                pass
            try:
                self.deliveryDate = df[1]["Scheduled Date"]
            except:
                self.deliveryDate = None
            
            #TODO
            self.returnedPackages:str = None
            
            Order.all_orders.append(self)
    
    def set_metadataId(self, metadataId:int) -> None:
        self.metadataId = metadataId

    @property
    def metadataId(self) -> int:
        return self._metadataId
        
    @metadataId.setter
    def metadataId(self, metadataId:int) -> None:
        self._metadataId = metadataId
    

class OrderItem:
    def __init__(self, sheetID:int = None, df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        try:
            self.product:Product = Product.all_products.search(productType=df[1]["Product Type"], displayName=df[1]["Product Display Name"], weight=float(df[1]["Weight"]),grind=df[1]["Product Grind"])[0]
        except:
            self.product:Product = None
        try:
            self.quantity = df[1]["Quantity"]
        except:    
            self.quantity = None
        try: 
            self.deliveryNote = df[1]["Delivery Note"]
        except:
            self.deliveryNote:bool = False
        try:
            self.lotNo = df[1]["LOT"]
        except:
            self.lotNo = None
        try:
            self.packaging = df[1]["Packaging"]
        except:
            self.packaging:str = False
        try:    
            self.packaged:bool = df[1]["Packaged"]
        except:
            self.packaged:bool = False
        try:
            self.sheetID = sheetID
        except:
            self.sheetID = None
            
        self.metadataId = None
        
        if sheetID != None:
            Order.all_orders.request_list += [{"createDeveloperMetadata": \
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

        Order(orderItem = self, df = df)
        
    def set_metadataId(self, metadataId:int) -> None:
        self.metadataId = metadataId

    @property
    def metadataId(self) -> int:
        return self._metadataId
        
    @metadataId.setter
    def metadataId(self, metadataId:int) -> None:
        self._metadataId = metadataId
        
    



    
