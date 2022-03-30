from typing import Optional, Tuple
from pandas import Series

class User:
    def __init__(self, sheet_df:Series = Series(dtype=(float))):
        try:
            self.firstName:str = sheet_df['First Name']
            self.lastName:str = sheet_df['Last Name']
            self.mmsUserID:str = sheet_df['MMS UserID']
            self.telegramUserID:int = int(sheet_df['Telegram UserID'])
            self.access:str = sheet_df['Access']    
        except:
            self.firstName:str = None
            self.lastName:str = None
            self.mmsUserID:str = None
            self.telegramUserID:int = None
            self.access:str = None
        
        
