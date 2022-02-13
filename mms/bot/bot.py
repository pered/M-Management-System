import logging
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update

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
    
    def message(self,update:Update, context:CallbackContext):
        update.message.reply_text("Hi")
    
    def event_handler(self) -> None:
        Bot.dispatcher.add_handler(CommandHandler("start", self.message))
    
    def start(self):
        Bot.updater.start_polling()
        Bot.updater.idle()