from .user import User
from typing import Tuple
from pandas import Series

class WholesaleUser(User):
    def __init__(self, df:Tuple[int, Series] = (None, Series(dtype=(float))), sheetID:int = None):
        super().__init__(df, sheetID)
        try:
            self.businessName:str = df[1]['Business Name']
        except:
            self.businessName:str = None
        
        
    
        
    
    