import logging
from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import Update

class Start:
    def begin(self) -> None:
        global updater, dispatcher
        updater = Updater("5026421018:AAGNBD_oSWKksgEyJpXkMQi0B6wx18pIVqU")
        dispatcher = updater.dispatcher
        logging.basicConfig(level=logging.INFO, 
                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    def start(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="I'm a bot, please talk to me!")
    
    def run(self):
        start_handler = CommandHandler('start', self.start)
        dispatcher.add_handler(start_handler)
        updater.start_polling()
    