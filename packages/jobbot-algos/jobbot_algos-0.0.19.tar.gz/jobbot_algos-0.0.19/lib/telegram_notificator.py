#!/usr/bin/env python
# coding: utf-8

# In[2]:


import telebot
import fastcore.basics as fcb


# In[3]:


def notify(text:str, chat_id=662822665):
    bot = telebot.TeleBot(token='6414971904:AAHEav0fiXV9_x4W3vtHI5RoJnIax7Oly8A')
    bot.send_message(chat_id, text, parse_mode="HTML")


# In[8]:


# notify('vd')

