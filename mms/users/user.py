from typing import Optional
from pandas import DataFrame

class User:
    def __init__(self):
        self.businessName:str = None
        self.firstName:str = None
        self.lastName:str = None
        self.userID:str = None
        self.access = None
        
    def sheetCreate(self, sheet_df:DataFrame) -> None:
        sheet_df.loc["MMS UserID"]
        
    def get_userID(self) -> str:
        return self.userID