from __future__ import print_function

import os.path

from google.oauth2 import service_account
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1mCJyUwHad0RBj14d8pvYC1EaCd4mHNwzkDKiUYTcLy4'
# SAMPLE_RANGE_NAME = 'Coffee!A2:E'

SAMPLE_SPREADSHEET_ID = "10bzoC_M0GOyEB8CH5zY9EXE7tGtxnC8vwJO3tTBDkyA"
SAMPLE_RANGE_NAME = 'Admin!A1:E'

creds = None
creds = service_account.Credentials.from_service_account_file('maximal-copilot-343018-f149332a7912.json',scopes=SCOPES)


service = build('sheets','v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()


get_spreadsheet_by_data_filter_request_body = {
    # The DataFilters used to select which ranges to retrieve from
    # the spreadsheet.
    'data_filters': {"a1Range":"Pere"},  # TODO: Update placeholder value.

    # True if grid data should be returned.
    # This parameter is ignored if a field mask was set in the request.
    'include_grid_data': False,  # TODO: Update placeholder value.

    # TODO: Add desired entries to the request body.
}

request = sheet.getByDataFilter(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=get_spreadsheet_by_data_filter_request_body)
response = request.execute()

print(response)

# # How the input data should be interpreted.
# value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

# value_range_body = {
#     "majorDimension" : 'ROWS',
#     "range" : "Admin!A3:E3",
#     "values": [['test ID','Name Test', 'Last Name Test', '0152842', 'Test']]
# }

# request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, valueInputOption=value_input_option, body=value_range_body)
# response = request.execute()

# # TODO: Change code below to process the `response` dict:
# print(response)
