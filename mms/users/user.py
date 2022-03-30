from typing import Optional, Tuple
from pandas import Series

class User:
    def __init__(self, sheet_df:Series = Series(dtype=(float))):
        try:
            self.firstName:str = sheet_df['First Name']
        except:
            self.firstName:str = None
            
        try: 
            self.lastName:str = sheet_df['Last Name']
        except:
            self.lastName:str = None
            
        try:
            self.mmsUserID:str = sheet_df['MMS UserID']
        except:
            self.mmsUserID:str = None
            
        try:
            self.telegramUserID:int = int(sheet_df['Telegram UserID'])
        except:
            self.telegramUserID:int = None
        
        try:
            self.access:str = sheet_df['Access']  
        except:
            self.access:str = None
        
        
