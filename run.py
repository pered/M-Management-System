import logging
from mms import Bot, Chats
from telegram.ext import CallbackContext
from telegram import Update
import json
    

def main() -> None:

    logging.basicConfig(level=logging.INFO, 
             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    mms_Bot = Bot()
    mms_Chats = Chats()
    
    mms_Bot.load()
    mms_Bot.start()


if __name__ == "__main__":
    main()