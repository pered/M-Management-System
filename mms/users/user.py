from typing import Optional

class User:
    def __init__(self):
        self.businessName:str = None
        self.firstName:str = None
        self.lastName:str = None
        self.userID:str = None
        self.access = None
        
    def get_userID(self) -> str:
        return self.userID