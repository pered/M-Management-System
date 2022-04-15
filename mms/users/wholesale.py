from ..businesslist import BusinessList
from ..businesses.business import Business
from .user import User
from typing import Tuple
from pandas import Series
import json

class WholesaleUser(User):
    def __init__(self, df:Tuple[int, Series] = (None, Series(dtype=(float))), sheetID:int = None):
        super().__init__(df, sheetID)
        try:
            self.business:Business = BusinessList.search(df[1]['Assigned Business'],"MMS Business ID")[0]
        except:
            self.business:Business = None
    

    
        
    
    