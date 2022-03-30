from typing import Optional,List
from telegram import Update, Chat, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import CallbackContext, CommandHandler,ChatMemberHandler, CallbackQueryHandler
from mms import HandlerList
from .userslist import UserList
import logging

class Chats:
    users:UserList = UserList()
    def __init__(self):
        super().__init__()
        Chats.users.load()
    
    ### Test functions ###
    
    def print_RegisteredUsers(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text([x.__dict__ for x in Chats.users.userList])
    
    def print_chatId(self,update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        data:Chat = update._effective_chat
        update.message.reply_text(data.id)
    
    def print_userId(self,update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        print(update.message.chat.id)
    
    ### Actual Programme Functions ###
    
    def send_help(self,update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Remind me to finish this!")
        
    #Admin Commands    
    
    def reload_Users(self, update: Update, context: CallbackContext) -> None:
        '''This function reloads all the users after there have been updates to\
            the data files on the cloud storage'''
        #Check if user is a super admin to perform command
        user:List = Chats.users.search(update.message.from_user.id, "Telegram UserID")
        if [True for x in user if x.access == "SuperAdmin"]:
            Chats.users.reload()
            update.message.reply_text("Reloaded all users!")
        else:
            update.message.reply_text("You are not worthy...")
    
   #Wholesale commands 
   
    def register(self, update: Update, context: CallbackContext) -> None:
        user:List = Chats.users.search(update.message.from_user.id, "Telegram UserID")
        
        if user == []:
            available_reg:List = Chats.users.search("Register", "Access")

            keyboard = [[InlineKeyboardButton(x.businessName, callback_data= x.businessName) \
                        for x in available_reg],
                        [InlineKeyboardButton("Cancel", callback_data='Cancel')],]
                
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Which cafe do you belong to?:', reply_markup=reply_markup)
            
            
        else:
            logging.info(f'User {update.message.from_user.name} with Telegram ID {update.message.from_user.id} is already registered')
   
    def register_action(self, update: Update, context: CallbackContext) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query
    
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()    
    
        if query.data == "Cancel":
            query.delete_message()
        
        elif type(query.data) == str:
            available_reg:List = Chats.users.search("Register", "Access")
            user_toAssign:List = [x for x in available_reg if x.businessName == query.data]
            
            
            
            if len(user_toAssign) == 1:
                user_toAssign[0].firstName = query.from_user.first_name
                user_toAssign[0].lastName = query.from_user.last_name
                # generate random mms id user_toAssing[0].mmsUserID =f'A{}'
                user_toAssign[0].telegramUserID = query.from_user.id
                user_toAssign[0].access = "Pending Approval"
                print(user_toAssign[0].__dict__)
                Chats.users.assign_User(user_toAssign)
                query.edit_message_text(text=f"You have been registered as: {query.data}")  
                
            else:
                logging.info("There are multiple businesses with the same business name to choose")
                query.edit_message_text(text="There's a problem, ask an admin to help")  
                
        
   
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



        


    def load(self):
        HandlerList(CommandHandler("chat_id", self.print_chatId))
        HandlerList(CommandHandler("user_id", self.print_userId))
        
        ### Actual Programme Handlers ###
        HandlerList(CommandHandler("help", self.send_help))
        
        #Admin Handlers
        HandlerList(CommandHandler("reload_users", self.reload_Users))
        
        #Wholesale Handlers
        HandlerList(CommandHandler('register', self.register))
        HandlerList(CallbackQueryHandler(self.register_action))
        
        HandlerList(CommandHandler('order', self.order))
        