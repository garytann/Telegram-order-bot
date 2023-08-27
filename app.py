from config import *

import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('bot_token')

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.contact = None
        self.email = None

def process_name_step(message):
    try:
        chat_id =  message.chat.id
        username = message.text # message obtain from user
        user = User(username)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Enter your contact details')
        bot.register_next_step_handler(msg, process_age_step)


    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_age_step(message):
    try:
        chat_id = message.chat.id
        contact = message.text
        if not contact.isdigit():
            msg = bot.reply_to(message, 'Contact details should contain only digits. Please try again.')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.contact = contact
        msg = bot.reply_to(message, 'Enter your email address')
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_email_step(message):
    try:
        chat_id = message.chat.id
        email = message.text
        user = user_dict[chat_id]
        user.email = email
        bot.send_message(chat_id, "Thank you for registering. You can now start ordering.", reply_markup=menu_keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
            Welcome to Inline Skating Class Registration.
                /register - register an account
                /menu - begin ordering
            """)
    
@bot.message_handler(commands=['register'])
def register_account(message):
    msg = bot.reply_to(message, "What is your name?")
    bot.register_next_step_handler(msg, process_name_step)
    
    
@bot.message_handler(commands=['menu'])
def send_menu(message):
    try:
        bot.reply_to(message, "Please select an option:", reply_markup=menu_keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')

bot.infinity_polling()


