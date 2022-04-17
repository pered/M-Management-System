#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 13:53:44 2022

@author: meister
"""

class Sheets:
    creds = service_account.Credentials.from_service_account_file(\
            'maximal-copilot-343018-f149332a7912.json',scopes=SCOPES)
    sheet = build('sheets','v4', credentials=creds).spreadsheets()   
    def __init__(self):
        pass