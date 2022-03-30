from typing import Optional,List
from telegram import Update, Chat, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import CallbackContext, CommandHandler,ChatMemberHandler, CallbackQueryHandler
from mms import HandlerList
from .userslist import UserList

class Chats:
    users:UserList = UserList()
    def __init__(self):
        super().__init__()
        Chats.users.load()

    def send_help(self,update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Remind me to finish this!")
    
    def print_RegisteredUsers(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text([x.__dict__ for x in Chats.users.userList])
    
    def check_userStatus(self,update: Update, context: CallbackContext) -> None:
        pass
    
    def reload_Users(self, update: Update, context: CallbackContext) -> None:
        #Check if user is a super admin to perform command
        user:List = Chats.users.search(update.message.from_user.id, "Telegram UserID")
        if [True for x in user if x.access == "SuperAdmin"]:
            Chats.users.load()
            update.message.reply_text("Reloaded all users!")
        else:
            update.message.reply_text("You are not worthy...")
    
    def print_chatId(self,update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        data:Chat = update._effective_chat
        update.message.reply_text(data.id)
    
    def print_userId(self,update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        print(update.message.chat.id)
        
    def order(self, update: Update, context: CallbackContext) -> None:
        """Sends a message with three inline buttons attached."""
        
        #Check what user is ordering, whether it's an Admin or Wholesale User
        
        #Check what chat it is and whether user corresponds with business
    
    
        keyboard = [
                    [InlineKeyboardButton("Coffee", callback_data='1'),
                    InlineKeyboardButton("Sugar", callback_data='2'),
                    InlineKeyboardButton("Milk", callback_data='4'),]
                    ,
                    [InlineKeyboardButton("Cancel", callback_data='Cancel'),
                     InlineKeyboardButton("Finish", callback_data='Finish')],
                    ]
    
        reply_markup = InlineKeyboardMarkup(keyboard)
    
        update.message.reply_text('What type of product do you want?:', reply_markup=reply_markup)


    def button(self, update: Update, context: CallbackContext) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query
    
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()
    
        query.edit_message_text(text=f"Selected option: {query.data}")
        


    def load(self):
        HandlerList(CommandHandler("help", self.send_help))
        HandlerList(CommandHandler("chat_id", self.print_chatId))
        HandlerList(CommandHandler("user_id", self.print_userId))
        HandlerList(CommandHandler("reload_users", self.reload_Users))
        HandlerList(CommandHandler('order', self.order))
        HandlerList(CallbackQueryHandler(self.button))
        #HandlerList(ChatMemberHandler(self.get_membersChange, ChatMemberHandler.CHAT_MEMBER))
        