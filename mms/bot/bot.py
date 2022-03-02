import logging
from typing import List
from telegram.ext import Updater
from telegram import Update

class HandlerList:
    handlers: List = []
    def __init__(self, handle):
        HandlerList.handlers.append(handle)

class Bot:
    updater:Updater = None
    dispatcher:Updater.dispatcher =  None
    logger:logging.getLogger =  None
    
    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO, 
                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        Bot.logger = logging.getLogger(__name__)
        Bot.updater = Updater("5026421018:AAGNBD_oSWKksgEyJpXkMQi0B6wx18pIVqU")
        Bot.dispatcher = Bot.updater.dispatcher

    
    def load(self) -> None:
        for handle in HandlerList.handlers:
            Bot.dispatcher.add_handler(handle)
    
    def start(self):
        Bot.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        Bot.updater.idle()