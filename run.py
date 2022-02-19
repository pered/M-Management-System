from mms import Bot, Customer
from telegram.ext import CallbackContext
from telegram import Update

def message(update:Update, context:CallbackContext):
    update.message.reply_text("Hi")
    

def main() -> None:
    mms_Bot = Bot()
    mms_Customer = Customer()
    mms_Bot.start()


if __name__ == "__main__":
    main()