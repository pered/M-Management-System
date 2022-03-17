from __future__ import print_function

import os.path

from google.oauth2 import service_account
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1mCJyUwHad0RBj14d8pvYC1EaCd4mHNwzkDKiUYTcLy4'
# SAMPLE_RANGE_NAME = 'Coffee!A2:E'

SAMPLE_SPREADSHEET_ID = "10bzoC_M0GOyEB8CH5zY9EXE7tGtxnC8vwJO3tTBDkyA"
SAMPLE_RANGE_NAME = 'Admin!A1:E'

creds = None
creds = service_account.Credentials.from_service_account_file('maximal-copilot-343018-f149332a7912.json',scopes=SCOPES)

def main():
    service = 
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    print(result)


if __name__ == '__main__':
    main()