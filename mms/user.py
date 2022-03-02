#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 12:56:05 2022

@author: meister
"""
from telegram import Update, Chat, ChatMemberUpdated
from telegram.ext import CallbackContext, CommandHandler,ChatMemberHandler
from mms import HandlerList

class User:
    def __init__(self):
        self.userId = None
        self.firstName = None
        
    def set_userID(self):
        self.userId
        

class Customer(User):
    def __init__(self):
        super()
        self.load()

    def print_chatId(self,update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        data:Chat = update._effective_chat
        update.message.reply_text(data.id)
        
        
    def get_membersChange(self,update: Update, context: CallbackContext) -> None:
        member_obj:ChatMemberUpdated = update.chat_member
        if member_obj != None:
            print(update.chat_member.to_json())
        else:
            pass

    def load(self):
        HandlerList(CommandHandler("chat_id", self.print_chatId))
        HandlerList(CommandHandler("members", self.get_membersChange))
        #HandlerList(ChatMemberHandler(self.get_membersChange, ChatMemberHandler.CHAT_MEMBER))
        