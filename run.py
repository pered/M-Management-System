import logging
from mms import Bot, Chats
from telegram.ext import CallbackContext
from telegram import Update
import json
    

def main() -> None:

    logging.basicConfig(level=logging.INFO, 
             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    #Initialise modules
    mms_Bot = Bot()
    mms_Chats = Chats()
    
    #Load Data from modules
    mms_Chats.load()
    mms_Bot.load()
    
    #Start bot
    mms_Bot.start()


if __name__ == "__main__":
    main()