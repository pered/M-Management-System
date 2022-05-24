import logging
from mms.bot import Bot
from mms.chats import Chats
from mms.users import User
from mms.business import Business
from mms.orders import Order
from mms.product import Product
from mms.settings import SettingsCFG

from telegram.ext import CallbackContext
from telegram import Update
import json


    

def main() -> None:

    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, 
             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger(__name__)
    logger.setLevel(logging.NOTSET)
    
    #Initialise modules
    mms_Bot = Bot()
    #Load the settings from the settings sheet in order to allow the dependent 
    #classes to initialise correctly (e.g. Chats)
    SettingsCFG.load()
    Product.all_products.load()
    Business.all_businesses.load()
    User.all_users.load()
    Order.all_orders.load()
    
    Chats.load()
    mms_Bot.load()
    
    #Start bot
    mms_Bot.start()


if __name__ == "__main__":
    main()