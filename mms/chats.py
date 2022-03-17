from typing import Optional
from telegram import Update, Chat, ChatMemberUpdated
from telegram.ext import CallbackContext, CommandHandler,ChatMemberHandler
from mms import HandlerList
from .userslist import UserList

class Chats:
    users: Optional[UserList] = UserList()
    def __init__(self):
        super()
        Chats.users.load()
        self.load()

    def send_help(self,update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Remind me to finish this!")
        
    def register_User(self, update: Update, context: CallbackContext) -> None:
        pass
        
    
    def print_chatId(self,update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        data:Chat = update._effective_chat
        update.message.reply_text(data.id)
    
    def print_userId(self,update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        data = update.message.from_user.id
        update.message.reply_text(data)
        


    def load(self):
        HandlerList(CommandHandler("help", self.send_help))
        HandlerList(CommandHandler("chat_id", self.print_chatId))
        HandlerList(CommandHandler("user_id", self.print_userId))
        #HandlerList(ChatMemberHandler(self.get_membersChange, ChatMemberHandler.CHAT_MEMBER))
        