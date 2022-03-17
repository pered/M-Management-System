from typing import Optional

class User:
    def __init__(self):
        self.businessName:str = None
        self.firstName:str = None
        self.lastName:str = None
        self.userID:str = None
        self.chatID:str = None
        self.orderAllowed = False
        
    def set_userID(self, userIDgiven:str):
        self.userID = userIDgiven
        
    def set_name(self, firstNamegiven:str, lastNamegiven:str = None):
        self.firstName = firstNamegiven
        self.lastName = lastNamegiven
        
    def set_chatID(self, chatIDgiven:str):
        self.chatID = chatIDgiven