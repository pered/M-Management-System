#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 12:56:05 2022

@author: meister
"""
from telegram import Update, Chat
from telegram.ext import CallbackContext, CommandHandler
from mms import Bot


class Customer:
    def __init__(self):
        self._declare()

    def add_customer(self,update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        data:Chat = update._effective_chat
        update.message.reply_text(data.id)
        
    def _declare(self, bot:Bot):
        bot.declare_handler(CommandHandler("test", self.add_customer))