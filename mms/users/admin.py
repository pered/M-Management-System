from .user import User
from pandas import Series

class Admin(User):
    def __init__(self, sheet_df:Series):
        super().__init__(sheet_df)
    
