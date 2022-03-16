from telegram import Update, Chat, ChatMemberUpdated
from telegram.ext import CallbackContext, CommandHandler,ChatMemberHandler
from mms import HandlerList
        

class Chats:
    def __init__(self):
        super()
        self.load()

    def send_help(self,update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Remind me to finish this!")
        
    def register_User(self, update: Update, context: CallbackContext) -> None:
        pass
        
    
    def print_chatId(self,update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        data:Chat = update._effective_chat
        update.message.reply_text(data.id)
        


    def load(self):
        HandlerList(CommandHandler("help", self.send_help))
        HandlerList(CommandHandler("chat_id", self.print_chatId))
        #HandlerList(ChatMemberHandler(self.get_membersChange, ChatMemberHandler.CHAT_MEMBER))
        