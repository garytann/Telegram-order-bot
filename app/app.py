from config import *

import telebot
from telebot import types
from telebot.custom_filters import AdvancedCustomFilter

import os
from dotenv import load_dotenv
import pdb
import json

load_dotenv()

API_TOKEN = os.getenv('bot_token')

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}
data_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.contact = None
        # self.email = None
        self.address = None

def process_name_step(message):
    try:
        chat_id =  message.chat.id
        username = message.text # message obtain from user
        user = User(username)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, """\
            In case I need to call you tonight, if you don't mind, 
            
            What's your contact number?
            """,
            reply_markup=reply_markup
            )
        bot.register_next_step_handler(msg, process_contact_step)

    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_contact_step(message):
    try:
        chat_id = message.chat.id
        contact = message.text
        if not contact.isdigit():
            msg = bot.reply_to(message, '😱 Oi contact details should contain only digits. Please try again.')
            bot.register_next_step_handler(msg, process_contact_step)
            return
        user = user_dict[chat_id]
        user.contact = contact
        msg = bot.reply_to(message, """\
            Okay, last question. I need to know where to send your order.
            
            What's your address?
            """, reply_markup=location_keyboard())
        # bot.register_next_step_handler(msg, process_pickup_address_step)
        # bot.reply_to(message, reply_markup=location_keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')

# def process_email_step(message):
#     try:
#         chat_id = message.chat.id
#         email = message.text
#         user = user_dict[chat_id]
#         user.email = email
#         msg = bot.reply_to(message, """\
#             Okay, last question. I need to know where to send your order.
#                 What's your address?
#             """)
#         bot.register_next_step_handler(msg, process_pickup_address_step)
#     except Exception as e:
#         bot.reply_to(message, 'oooops')

# def process_pickup_address_step(message):
#     try:
        # bot.send_message(message, reply_markup=location_keyboard())
        # chat_id = message.chat.id
        # address = message.text
        # user = user_dict[chat_id]
        # user.address = address

        # content = {
        #     "name": user.name,
        #     "contact": user.contact,
        #     "email": user.email,
        #     "address": user.address
        # }

        # if chat_id in data_dict:
        #     data_dict[chat_id].append(content)
        # else:
        #     data_dict[chat_id] = content
        # # pdb.set_trace()
        # # Save data_dict into a JSON file
        # json_file_path = "data.json"
        # with open(json_file_path, "w") as json_file:
        #     json.dump(data_dict, json_file, indent=4)
        # bot.send_message(chat_id, "Thank you for registering. You can now start ordering.", reply_markup=menu_keyboard())
    # except Exception as e:
    #     msg =  bot.reply_to(message, 'oooops. Please try again')
    #     bot.register_next_step_handler(msg, process_pickup_address_step)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    # Load data from the JSON file
    json_file_path = "../data/data.json"
    with open(json_file_path, "r") as json_file:
        records = json.load(json_file)

    if str(message.chat.id) in records:
        name_value = records[str(message.chat.id)]["name"]
        bot.send_message(chat_id, f"Hey {(name_value).lower()}, craving for Açaí again? ", reply_markup=menu_keyboard())
    else:
        bot.reply_to(message, """\
                Hi! I'm AçaíBot. We can't wait for you to try our Açaí!
            
                But first, we need to know a few things about you.
                """,
                reply_markup=register_keyboard()
                )
    
# @bot.message_handler(commands=['register'])
# def register_account(message):
#     msg = bot.reply_to(message, """\
#             You're not Karen or Ken, are you? 
#                 Enter your name below.
#             """)
#     bot.register_next_step_handler(msg, process_name_step)
    
    
@bot.message_handler(commands=['menu'])
def send_menu(message):
    try:
        bot.reply_to(message, "Please select an option:", reply_markup=menu_keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')

# Register Callback
@bot.callback_query_handler(func=None, config=register_factory.filter())
def register_callback(call: types.CallbackQuery):
    callback_data : dict = register_factory.parse(callback_data=call.data)
    register_id = int(callback_data['register_id'])
    register = REGISTRATION[register_id]

    # Register
    if (register['id'] == '0'):
        msg = bot.reply_to(call.message, """\
            You're not Karen or Ken, are you? 
            
            Enter your name below.
            """,
            reply_markup=reply_markup
            )
        bot.register_next_step_handler(msg, process_name_step)
    else:
        pass

# Menu Callback
@bot.callback_query_handler(func=None, config=menu_factory.filter())
def menu_callback(call: types.CallbackQuery):
    callback_data : dict = menu_factory.parse(callback_data=call.data)
    product_id = int(callback_data['menu_id'])
    menu = MENU[product_id]

    # Order
    if (menu['id'] == '0'):
        bot.reply_to(call.message,f"Select your order: ", reply_markup=order_keyboard())
    else:
        pass

# Pick up address Callback
@bot.callback_query_handler(func=None, config=location_factory.filter())
def location_callback(call: types.CallbackQuery):
    callback_data : dict = location_factory.parse(callback_data=call.data)
    product_id = int(callback_data['location_id'])
    location = LOCATION[product_id]
    # pdb.set_trace()

    chat_id = call.message.chat.id
    user = user_dict[chat_id]
    user.address = location['name']

    content = {
        "name": user.name,
        "contact": user.contact,
        "address": user.address
    }
    # pdb.set_trace()

    if chat_id in data_dict:
        data_dict[chat_id].append(content)
    else:
        data_dict[chat_id] = content
    # pdb.set_trace()
    # Save data_dict into a JSON file
    json_file_path = "../data/data.json"
    with open(json_file_path, "w") as json_file:
        json.dump(data_dict, json_file, indent=4)
    bot.send_message(chat_id, "Thank you for registering. You can now start ordering.", reply_markup=menu_keyboard())
        


# Order Callback

if __name__ == "__main__":
    print('app started')
    bot.add_custom_filter(ProductsCallbackFilter())
    bot.infinity_polling()


