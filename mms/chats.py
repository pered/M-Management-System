from typing import Optional,List
import random
import string
from telegram import Update, Chat, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import CallbackContext, CommandHandler,ChatMemberHandler, CallbackQueryHandler, ConversationHandler,MessageHandler, Filters
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
            Chats.users.reload_all()
            update.message.reply_text("Reloaded all users!")
        else:
            update.message.reply_text("You are not worthy...")
    
   #Wholesale commands 
   
    def cancel(self, update: Update, context: CallbackContext) -> int:
        """Cancels and ends the conversation."""
        user = update.message.from_user
        logging.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.')
        
        return ConversationHandler.END
   
    def register(self, update: Update, context: CallbackContext) -> str:
        '''Function that provides the ability for wholesale to register in a previously
        created wholesale user slot in cloud server database'''
        
        #Check if user is registered as anything
        userlist:List = Chats.users.search(update.message.from_user.id, "Telegram UserID")
        #If the user is not registered then provide registration options with
        #businesses that have been created with "Register" access in cloud server
        
        if userlist == []:
            available_reg:List = Chats.users.search("Register", "Access")

            keyboard = [[InlineKeyboardButton(x.businessName, callback_data= x.businessName) \
                        for x in available_reg],
                        [InlineKeyboardButton("Cancel", callback_data='Cancel')],]
                
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Which cafe do you belong to?:', reply_markup=reply_markup)
         
            return "REGISTER"
        #Else we check whether the user is "Pending Approval" or has already been registered
        else:
            #Refresh in case there has been status change
            [users.refresh() for users in userlist]
            pending_users:List = Chats.users.search("Pending Approval", "Access", userlist)
            
            if [True for user in pending_users if user.access == 'Pending Approval']:
                update.message.reply_text('Please wait for you registration to be approved')
                logging.info(f'User {update.message.from_user.name} with Telegram ID {update.message.from_user.id} is awaiting approval!')
                return ConversationHandler.END
            else:
                try:
                    [update.message.reply_text(f'You are already registered as {user.businessName}') for user in userlist]
                except:
                    [update.message.reply_text('You are already registered as {user.firstName} with access level of {user.access}') for user in userlist]
                logging.info(f'User {update.message.from_user.name} with Telegram ID {update.message.from_user.id} is already registered.')
                return ConversationHandler.END
            
        
    
    def register_query(self, update: Update, context: CallbackContext) -> int:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query
    
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()
    
        if query.data == "Cancel":
            query.delete_message()
        
        elif type(query.data) == str:
            
            available_reg:List = Chats.users.search("Register", "Access")
            user_toAssign:List = Chats.users.search(query.data, "Business Name", available_reg)
            
            if len(user_toAssign) == 1:
                
                user_toAssign[0].firstName = query.from_user.first_name
                user_toAssign[0].lastName = query.from_user.last_name
                user_toAssign[0].mmsUserID = 'A'+''.join(random.choices(string.ascii_letters + string.digits, k=5))
                user_toAssign[0].telegramUserID = query.from_user.id
                user_toAssign[0].access = "Pending Approval"
                print(user_toAssign[0].__dict__)
                user_toAssign[0].save()
                
                query.edit_message_text(text=f"You have been registered as: {query.data}")  
                
            else:
                
                logging.info("There are multiple businesses with the same business name to choose")
                query.edit_message_text(text="An error has been recorded!")  
                
        return ConversationHandler.END
   
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
        HandlerList(CommandHandler('userlist', self.print_RegisteredUsers))
        
        ### Actual Programme Handlers ###
        HandlerList(CommandHandler("help", self.send_help))
        
        #Admin Handlers
        HandlerList(CommandHandler("reload_users", self.reload_Users))
        
        #Wholesale Handlers
        HandlerList(ConversationHandler(entry_points=[
                                            CommandHandler('register', self.register)],
                                        states={"REGISTER":[
                                            CallbackQueryHandler(self.register_query)]},
                                        fallbacks=[CommandHandler('cancel', self.cancel)]))     
        
        #CommandHandler('order', self.order)],