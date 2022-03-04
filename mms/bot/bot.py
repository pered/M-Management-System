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

    def __init__(self) -> None:
        Bot.updater = Updater("5026421018:AAGNBD_oSWKksgEyJpXkMQi0B6wx18pIVqU")
        Bot.dispatcher = Bot.updater.dispatcher

    
    def load(self) -> None:
        for handle in HandlerList.handlers:
            Bot.dispatcher.add_handler(handle)
    
    def start(self):
        Bot.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        Bot.updater.idle()