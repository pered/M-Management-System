from .. import ProductList
from typing import List,Tuple,Dict, overload
from pandas import Series, DataFrame
import logging

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