from mms.ext import Sheets
from typing import List,Tuple,Dict, overload
from pandas import Series, DataFrame
import logging

class ProductList(Sheets, list['Product']):
    SPREADSHEET_ID = "1mCJyUwHad0RBj14d8pvYC1EaCd4mHNwzkDKiUYTcLy4"
    sheet_info = [{"Range": "COFFEE",
                    "sheetID": 0},
                  {"Range": "SUGAR",
                    "sheetID": 1980308451},
                  {"Range" : "BEVERAGES", 
                    "sheetID": 366404389}]

    def __init__(self):
        Sheets.__init__(self)
    
    def load(self):
        #If productlist has values in itself, then delete them all and reload
        if Product.all_products.__len__() != 0:
            Product.all_products.clear()
            logging.info("Reloaded product list")
        
        #From sheets obtain results from sheet
        self.results = Sheets.load(self)
        
        #Create a list of objects with products in them
        [[Product(ProductList.sheet_info[index]['Range'],sf_product)
          for sf_product in df_product.iterrows()] 
             for index, df_product in [(self.results['valueRanges'].index(productRange),DataFrame(productRange['values'][1:], columns = productRange['values'][0])) 
                                       for productRange in self.results['valueRanges']]]
    
    
    def search(self, productType = None, displayName:str = None, weight:float = None, grind:str = None, product_toSearch:List = None) -> List:
        '''This function returns objects that match the value with the given attribute'''
        if product_toSearch == None:
            product_toSearch = Product.all_products
        
        try:
            search_results = list(filter(lambda z: (productType == None or z.productType == productType), product_toSearch))
            search_results = list(filter(lambda z: (displayName == None or z.displayName == displayName), search_results))
            if weight != None:
                search_results = list(filter(lambda z: (weight == None or z.weight == weight), list(filter(lambda x: hasattr(x, "weight"), search_results))))
            search_results = list(filter(lambda z: (grind == None or z.grind == grind), search_results))
            return search_results
        except:
            raise ValueError("Tried to seach for an invalid weight in products")
            return []


class Product:
    all_products = ProductList()
    
    def __init__(self, productType:str = None,df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        if productType == 'COFFEE':
            Coffee(productType, df)
            
        elif productType == 'SUGAR':
            Sugar(productType, df)
            
        elif productType == 'BEVERAGES':
            Beverages(productType, df)
            
        
class Coffee(Product):
    def __init__(self,productType:str = None,df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        logging.info("Initializing coffee product")
        if productType != None:
            self.productId:str = df[1]['Product ID']
            self.displayName:str = df[1]['Display Name']
            self.farmName:str = df[1]['Farm']
            self.productType = productType
            self.origin:str = df[1]['Origin']
            self.grind:str = df[1]['Grinds']
            self.weight:float = float(df[1]['Weight'])
            self.price:float = float(df[1]['Price'])
            self.availability:str = df[1]['Availability']
            Product.all_products.append(self)
    
class Sugar(Product):
    def __init__(self,productType:str = None,df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        logging.info("Initializing sugar product")
        if productType != None:
            self.productId:str = df[1]['Product ID']
            self.displayName:str = df[1]['Display Name']
            self.productName:str = df[1]['Product Name']
            self.productType = productType
            self.variety:str = df[1]['Type Variety']
            self.quantity:str = df[1]['Quantity']
            self.price:float = float(df[1]['Price'])
            self.availability:str = df[1]['Availability']
            
            Product.all_products.append(self)
            
class Beverages(Product):
    def __init__(self,productType:str = None,df:Tuple[int, Series] = (None, Series(dtype=(float)))):
        logging.info("Initializing beverage product")
        if productType != None:
            self.productId:str = df[1]['Product ID']
            self.displayName:str = df[1]['Display Name']
            self.productName:str = df[1]['Product Name']
            self.productType = productType
            self.variety:str = df[1]['Type Variety']
            self.quantity:str = df[1]['Quantity']
            self.price:float = float(df[1]['Price'])
            self.availability:str = df[1]['Availability']
            
            Product.all_products.append(self)