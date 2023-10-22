from config import *

import telebot
from telebot import types
from telebot.custom_filters import AdvancedCustomFilter

import os
from dotenv import load_dotenv
import pdb
import json
import requests
from datetime import datetime

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
HOST_IP = os.getenv('HOST_IP')

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
            
        Where do I deliver?
        """, 
        reply_markup=location_keyboard())

        # bot.register_next_step_handler(msg, process_pickup_address_step)
        # bot.reply_to(message, reply_markup=location_keyboard())
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    userid_exists = False

    # make a GET request to the accounts API endpoint
    try:
        account_list_endpoint = f"http://{HOST_IP}:8000/accounts/accounts"
        response = requests.get(account_list_endpoint)
        response.raise_for_status()
        if response.status_code == 200:
            accounts = response.json()
        else:
            pass
    except requests.RequestException as e:
        bot.reply_to(message, f"Error connecting to the API {HOST_IP}")
        return
    except ValueError as e:
        bot.reply_to(message, "Error decoding response JSON")
        return

    for account in accounts:
        if account['userid'] == str(chat_id):
            userid_exists = True
            break
    
    if userid_exists:
        bot.send_message(chat_id, "Welcome back! What would you like to order?", reply_markup=menu_keyboard())
    else:
        bot.reply_to(message, """\
        Hi! I'm AçaíBot. We can't wait for you to try our Açaí!
            
        But first, we need to know a few things about you.
        """,
            reply_markup=register_keyboard()
            )
    
    
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
        "address": str(user.address),
        "contact": str(user.contact),
        "name": str(user.name),
        "userid": str(chat_id)
    }


    # double check if the user has already registered
    if chat_id in data_dict:
        data_dict[chat_id].append(content)
    else:
        data_dict[chat_id] = content

    account_registeration_endpoint = f"http://{HOST_IP}:8000/accounts/register"
    
    try:
        response = requests.post(account_registeration_endpoint, json=content)
        response.raise_for_status()
        if response.status_code == 201:
            created_account = response.json()
            bot.send_message(chat_id, "Thank you for registering. You can now start ordering.", reply_markup=menu_keyboard())
        else:
            pass
    except requests.exceptions.RequestException as e:
        print(f"Error sending registration request: {e}")
    except ValueError as e:
        print(f"Error parsing response: {e}")
    
# Order Callback
@bot.callback_query_handler(func=None, config=order_factory.filter())
def order_callback(call: types.CallbackQuery):
    callback_data : dict = order_factory.parse(callback_data=call.data)
    product_id = int(callback_data['order_id'])
    order = ORDER[product_id]
    chat_id = call.message.chat.id
    userid_exists = False
    
    # Get account details based on chat_id
    account_list_endpoint = f"http://{HOST_IP}:8000/accounts/accounts"
    try:
        response = requests.get(account_list_endpoint)
        response.raise_for_status()
        if response.status_code == 200:
            accounts = response.json()
        else:
            pass
    except requests.RequestException as e:
        bot.reply_to(call.message, "Error connecting to the API")
        return
    except ValueError as e:
        bot.reply_to(call.message, "Error decoding response JSON")
        return
    
    account_exists = [account for account in accounts if account['userid'] == str(chat_id)]

    if account_exists:
        # Assuming there's at most one matching account, you can access its values
        account_exists = account_exists[0]
        name_value = account_exists["name"]
        contact_value = account_exists["contact"]
        address_value = account_exists["address"]
        userid_value = account_exists["userid"]

        # fill up the order details as a dictionary
        content = {
            # "date": str(datetime.now().strftime("%d-%m-%Y")),
            "order": str(order['name']),
            "name": str(name_value),
            "address": str(address_value),
            "userid": str(userid_value)
        }

        order_endpoint = f"http://{HOST_IP}:8000/orders/createorders"

        try:
            response = requests.post(order_endpoint, json=content)
            response.raise_for_status()
            if response.status_code == 201:
                created_order = response.json()

                # CHANGE ORDER FUNCTION WIP
                # bot.send_message(chat_id, f"Your order {order['name']} has been placed. Thank you for ordering.", 
                #                  reply_markup=order_menu_keyboard())
                bot.send_message(chat_id, f"Your order {order['name']} has been placed. Thank you for ordering.")
            else:
                pass
        except requests.exceptions.RequestException as e:
            print(f"Error sending order request: {e}")
        except ValueError as e:
            print(f"Error parsing response: {e}")

# Order Menu Callback
@bot.callback_query_handler(func=None, config=order_menu_factory.filter())
def order_menu__callback(call: types.CallbackQuery):
    callback_data : dict = order_menu_factory.parse(callback_data=call.data)
    product_id = int(callback_data['order_menu_id'])
    order_menu_id = ORDER_MENU[product_id]
    chat_id = call.message.chat.id

    if (order_menu_id['id'] == '0'):
        # handle update order
        # user chat_id to fetch the user's order
        # need to ask user what they want to update
        bot.send_message(chat_id,f"Your order has been updated successfully!")
    else:
        # handle cancel the order
        bot.send_message(chat_id,f"What a waste... Your order has been canceled successfully!")


if __name__ == "__main__":
    print('TELEGRAAM APP DEPLOYED')
    bot.add_custom_filter(ProductsCallbackFilter())
    bot.infinity_polling()


