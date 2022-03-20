from .user import User
from pandas import DataFrame

class Admin(User):
    def __init__(self, sheet_df:DataFrame):
        super().__init__(sheet_df)
    
