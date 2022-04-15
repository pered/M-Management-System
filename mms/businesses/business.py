from typing import Tuple
from pandas import Series
import logging
from .. import businesslist
import json

class Business:
    def __init__(self, df:Tuple[int, Series] = (None, Series(dtype=(float))), sheetID:int = None):
        try:
            self.mmsbusinessId = df[1]['MMS Business ID']
        except:
            self.mmsbusinessId = None
            
        try:
            self.telegramChatId = df[1]['Telegram Chat ID']
        except:
            self.telegramChatId = None
        
        try:
            self.businessName = df[1]['Business Name']
        except:
            self.businessName = None
            
        self.metadataId = None
        
        if sheetID != None:
            businesslist.BusinessList.request_list += [{"createDeveloperMetadata": \
                                                 {"developerMetadata": {
                                                     "metadataKey": "sheetID"+f"{df[0]+1}",
                                                     "location" : {"dimensionRange":
                                                                   {"sheetId":sheetID,
                                                                    "dimension":"ROWS",
                                                                    "startIndex": df[0]+1,
                                                                    "endIndex": df[0]+2}
                                                                   },
                                                     "visibility": "DOCUMENT"}
                                                         }}]
            logging.info(f"Created type {type(self)} with name {self.businessName}")
            
    def set_metadataId(self,metadataId:int) -> None:
        self.metadataId = metadataId
            
    def save(self)-> None:
        batch_datafilter_update = {"valueInputOption": 'USER_ENTERED',
                                    "data": [{"dataFilter": {'developerMetadataLookup': 
                                                            {'metadataId': self.metadataId
                                                            }},
                                    "majorDimension": 'ROWS',
                                    "values": [[self.mmsbusinessId, self.telegramChatId, self.businessName]
                                                ]}]}
            
        businesslist.BusinessList.sheet.values().batchUpdateByDataFilter(spreadsheetId=businesslist.BusinessList.SAMPLE_SPREADSHEET_ID, body=batch_datafilter_update).execute()
        
    def refresh(self) -> None:
        batch_request_get = {

            'data_filters': [{'developerMetadataLookup': {'metadataId': self.metadataId
                                                          }}]  # TODO: Update placeholder value.

        }
        
        response = businesslist.BusinessList.sheet.values().batchGetByDataFilter(spreadsheetId=businesslist.BusinessList.SAMPLE_SPREADSHEET_ID, body = batch_request_get).execute()
        self.mmsbusinessId, self.telegramChatId,self.businessName = response['valueRanges'][0]['valueRange']['values'][0]
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)