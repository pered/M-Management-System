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
ADMIN_SAMPLE_RANGE_NAME = 'Admin'
WHOLESALE_SAMPLE_RANGE_NAME = 'Wholesale'

creds = None
creds = service_account.Credentials.from_service_account_file('maximal-copilot-343018-f149332a7912.json',scopes=SCOPES)


service = build('sheets','v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().batchGet(spreadsheetId=SAMPLE_SPREADSHEET_ID, ranges=[ADMIN_SAMPLE_RANGE_NAME,WHOLESALE_SAMPLE_RANGE_NAME])
response = result.execute()

print([i['values'] for i in response['valueRanges']])


# create_developer_metadata = {"requests" :[{"createDeveloperMetadata": {"developerMetadata": {
#                                                                  "metadataKey":"Pere",
#                                                                  "location" : {"dimensionRange":
#                                                                                {"sheetId":1929008158,
#                                                                                "dimension":"ROWS",
#                                                                                "startIndex": 1,
#                                                                                "endIndex": 2}
#                                                                                },
#                                                                  "visibility": "DOCUMENT"}
#      }},
#                                             {"createDeveloperMetadata": {"developerMetadata": {
#                                                                  "metadataKey":"Test",
#                                                                  "location" : {"dimensionRange":
#                                                                                {"sheetId":1929008158,
#                                                                                "dimension":"ROWS",
#                                                                                "startIndex": 2,
#                                                                                "endIndex": 3}
#                                                                                },
#                                                                  "visibility": "DOCUMENT"}
#      }}]}

# request = service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=create_developer_metadata)
# response = request.execute()

# #This is one way of looking up metadata
# batch_get_values_by_data_filter_request_body = {

#     'data_filters': [{'developerMetadataLookup': {'metadataId': 1138576308,
#                                                   'metadataLocation' : {"sheetId":1929008158}
#                                                   }}]  # TODO: Update placeholder value.

# }

# request = sheet.values().batchGetByDataFilter(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=batch_get_values_by_data_filter_request_body)
# response = request.execute()

#Another way of getting metadata by ID
# request = sheet.developerMetadata().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,metadataId=1167760412)
# response = request.execute()


# #This deletes all previously applied metadata on a sheet
# delete_all = {"requests" :{"deleteDeveloperMetadata":{"dataFilter": {"developerMetadataLookup": {"metadataLocation": {"sheetId":1929008158}}}}}}
# request = service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=delete_all)
# response = request.execute()

#Updating values by the use of metadata ID

# batch_datafilter_update = {"valueInputOption": 'USER_ENTERED',
#                            "data": [{"dataFilter": {'developerMetadataLookup': 
#                                                    {'metadataId': 265876189
#                                                     }},
#                             "majorDimension": 'ROWS',
#                             "values": [[None,'Ok',None,None,None]
#                                        ]}]}

# request = sheet.values().batchUpdateByDataFilter(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=batch_datafilter_update)
# response = request.execute()

#print(response)