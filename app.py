from config import *

import telebot
from telebot import types
import os
from dotenv import load_dotenv
import pdb

load_dotenv()

API_TOKEN = os.getenv('bot_token')

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}
data_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.contact = None
        self.email = None
        self.address = None

def process_name_step(message):
    try:
        chat_id =  message.chat.id
        username = message.text # message obtain from user
        user = User(username)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, """\
            In case I need to call you tonight, if you don't mind, 
                what's your contact number?
            """)
        bot.register_next_step_handler(msg, process_contact_step)


    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_contact_step(message):
    try:
        chat_id = message.chat.id
        contact = message.text
        if not contact.isdigit():
            msg = bot.reply_to(message, 'Contact details should contain only digits. Please try again.')
            bot.register_next_step_handler(msg, process_contact_step)
            return
        user = user_dict[chat_id]
        user.contact = contact
        msg = bot.reply_to(message, """\
            Who still uses email? But maybe there will be freebies who knows. 
                What's your email address?
            """)
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_email_step(message):
    try:
        chat_id = message.chat.id
        email = message.text
        user = user_dict[chat_id]
        user.email = email
        msg = bot.reply_to(message, """\
            Okay, last question. I need to know where to send your order.
                What's your address?
            """)
        bot.register_next_step_handler(msg, process_pickup_address_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_pickup_address_step(message):
    try:
        chat_id = message.chat.id
        address = message.text
        user = user_dict[chat_id]
        user.address = address

        content = {
            "name": user.name,
            "contact": user.contact,
            "email": user.email,
            "address": user.address
        }
        if chat_id in data_dict:
            data_dict[chat_id].append(content)
        else:
            data_dict[chat_id] = content
        pdb.set_trace()
        bot.send_message(chat_id, "Thank you for registering. You can now start ordering.", reply_markup=menu_keyboard())
    except Exception as e:
        msg =  bot.reply_to(message, 'oooops. Please try again')
        bot.register_next_step_handler(msg, process_pickup_address_step)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    pdb.set_trace()
    bot.reply_to(message, """\
            Welcome to ACAI
                /register - enter your details
                /menu - begin ordering
            """)
    
@bot.message_handler(commands=['register'])
def register_account(message):
    msg = bot.reply_to(message, """\
        We can't wait for you to try our ACAI!
        But first, we need to know a few things about you.
            You're not Karen or Ken, are you? Enter your name below.
            """)
    bot.register_next_step_handler(msg, process_name_step)
    
    
@bot.message_handler(commands=['menu'])
def send_menu(message):
    try:
        bot.reply_to(message, "Please select an option:", reply_markup=menu_keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')

bot.infinity_polling()


