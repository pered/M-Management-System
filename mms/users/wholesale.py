from .user import User
from pandas import Series

class WholesaleUser(User):
    def __init__(self, sheet_df:Series = Series(dtype=(float))):
        super().__init__(sheet_df)
        try:
            self.businessName:str = sheet_df['Business Name']
        except:
            self.businessName:str = None
        
        
    
        
    
    