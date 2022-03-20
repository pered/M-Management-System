from typing import Optional, Tuple
from pandas import Series

class User:
    def __init__(self, sheet_df:Series):
        self.firstName = sheet_df['First Name']
        self.lastName = sheet_df['Last Name']
        self.mmsUserID = sheet_df['MMS UserID']
        self.telegramUserID = sheet_df['Telegram UserID']
        self.access = sheet_df['Access']
