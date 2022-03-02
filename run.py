from mms import Bot, Customer
from telegram.ext import CallbackContext
from telegram import Update

    

def main() -> None:
    mms_Bot = Bot()
    mms_Customer = Customer()
    mms_Bot.load()
    mms_Bot.start()


if __name__ == "__main__":
    main()