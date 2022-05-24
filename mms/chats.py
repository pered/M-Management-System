from typing import Optional,List
import logging
import json
import random
import string

from telegram import Update, Chat, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import CallbackContext, CommandHandler,ChatMemberHandler, CallbackQueryHandler, ConversationHandler,MessageHandler, Filters

from .users import User
from .business import Business
from .orders import Order
from .settings import SettingsCFG
from .bot import HandlerList



class Chats:
    def __init__(self):
        pass
        
    ### Test functions ###
    
    def print_chatId(update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        data:Chat = update._effective_chat
        update.message.reply_text(data.id)
    
    def print_userId(update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        print(update.message.chat.id)
        
    def print_userList(update: Update, context: CallbackContext) -> None:
        print(User.all_users.print())
    
    ### Actual Programme Functions ###

    @classmethod
    def send_help(update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Remind me to finish this!")
        
    #Admin Commands    
    
    def reload_users(update: Update, context: CallbackContext) -> None:
        '''This function reloads all the users after there have been updates to\
            the data files on the cloud storage'''
        #Check if user is a super admin to perform command
        user:List = User.all_users.search(telegramUserID=str(update.message.from_user.id))
        if [True for x in user if x.access == "SuperAdmin"]:
            User.all_users.load()
            update.message.reply_text("Reloaded all users!")
        else:
            update.message.reply_text("You do not have admin rights")
    
   #Wholesale commands 
   
    @classmethod
    def register(cls, update: Update, context: CallbackContext) -> str:
        '''Function that provides the ability for wholesale to register in a previously
        created wholesale user slot in cloud server database'''
        
        #Check if user is registered as anything
        usermatch_telegramId:List = cls.users.search(update.message.from_user.id, "Telegram UserID")
        print(usermatch_telegramId)
        #If the user is not registered then provide registration options with
        #businesses that have been created with "Register" access in cloud server
        
        if len(usermatch_telegramId) < SettingsCFG.max_reg_per_user:
            #If the amount of links between the telegram user id is less than the maximum allowed
            #we proceed to refresh those users to check if their status has changed
            
            [users.refresh() for users in usermatch_telegramId]
            pending_users:List = cls.users.search("Pending Approval", "Access", usermatch_telegramId)
    
            if [True for user in pending_users if user.access == 'Pending Approval']:
                
                #and if any of the users returned are pending approval we tell them to wait
                
                update.message.reply_text('We are getting your registration approved')
                logging.info(f'User {update.message.from_user.name} with Telegram ID {update.message.from_user.id} is awaiting approval!')
                return ConversationHandler.END
            
            else:
                
                #and if the users are not waiting to be approved and under the 
                #limit we allow them to register for some open spots
                
                available_reg:List = Chats.users.search("Register", "Access")
    
                keyboard = [[InlineKeyboardButton(x.business.businessName, callback_data= x.business.businessName) \
                            for x in available_reg],
                            [InlineKeyboardButton("Cancel", callback_data='Cancel')],]
                    
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('Which cafe do you belong to?:', reply_markup=reply_markup)
             
                return "REGISTER"
        
        #Otherwise we tell them they are over the limit and tell them to stop
        
        elif len(usermatch_telegramId) >= SettingsCFG.max_reg_per_user:
            update.message.reply_text('You have reached the maximum allowed registrations!')
            logging.info(f'User {update.message.from_user.name} with Telegram ID {update.message.from_user.id} has reached maximum registrations!')
            return ConversationHandler.END
        
        #As of writing this I am tired and not able to think of cases that would fill this
        else:
            logging.info('Check register definition for unusual registration case')
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
                user_toAssign[0].telegramUserID = str(query.from_user.id)
                user_toAssign[0].access = "Pending Approval"
                user_toAssign[0].save()
                try:
                    user_toAssign[0].business.telegramChatId = str(query.message.chat_id)
                    user_toAssign[0].business.save()
                except:
                    pass
                
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



    def load():
        
        #Load Handlers
        HandlerList(CommandHandler("chat_id", Chats.print_chatId))
        HandlerList(CommandHandler("user_id", Chats.print_userId))
        HandlerList(CommandHandler('print_userlist', Chats.print_userList))
        
        ### Actual Programme Handlers ###
        HandlerList(CommandHandler("help", Chats.send_help))
        
        #Admin Handlers
        HandlerList(CommandHandler("reload_users", Chats.reload_users))
        
        #Wholesale Handlers
        #HandlerList(ConversationHandler(entry_points=[
        #                                    CommandHandler('register', Chats.register)],
        #                                states={"REGISTER":[
        #                                    CallbackQueryHandler(Chats.register_query)]},
        #                                fallbacks=[]))     
        
        #CommandHandler('order', self.order)],