from telebot import types
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

reply_markup = types.ForceReply(selective=False)


MENU = [
    {'id': '0', 'name': 'Order',},
    # {'id': '1', 'name': 'Check Order Status'},
    # {'id': '2', 'name': 'Cancel Order'},
    {'id': '1', 'name': 'Settings'},
    {'id': '2', 'name': 'Exit'}
]

ORDER = [
    {'id': '0', 'name': 'Option 1',},
    {'id': '1', 'name': 'Option 2'},
]

REGISTRATION = [
    {'id': '0', 'name': 'Register',},
]

LOCATION = [
    {'id': '0', 'name': 'Hall 8 Admin Office',},
    {'id': '1', 'name': 'Hall 11 Drop Off Point',},
    {'id': '2', 'name': 'North Hill Carpark',},
    {'id': '3', 'name': 'Tamarind/Saraca Drop Off Point',},
    {'id': '4', 'name': 'Hall 14 Drop Off Point',},
    {'id': '5', 'name': 'Hall 12 Amphitheatre',},
    {'id': '6', 'name': 'Hall 3 Admin Office',},
    {'id': '7', 'name': 'Canteen 2 Walkway',},
    {'id': '8', 'name': 'Hall 6 Drop Off Point',},
    {'id': '9', 'name': 'Crescent Hall Drop Off Point',},
    {'id': '10', 'name': 'Hall 5 Drop Off Point',},
    {'id': '11', 'name': 'Hall 4 Drop Off Point',},
]


register_factory = CallbackData('register_id', prefix='register')
order_factory = CallbackData('order_id', prefix='order')
menu_factory = CallbackData('menu_id', prefix='menu')
location_factory = CallbackData('location_id', prefix='location')

def location_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=item['name'],
                    callback_data=location_factory.new(location_id=item["id"])
                )
            ]
            for item in LOCATION
        ]
    )

def menu_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=item['name'],
                    callback_data=menu_factory.new(menu_id=item["id"])
                )
            ]
            for item in MENU
        ]
    )

def order_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=item['name'],
                    callback_data=order_factory.new(order_id=item["id"])
                )
            ]
            for item in ORDER
        ]
    )

def register_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=item['name'],
                    callback_data=register_factory.new(register_id=item["id"])
                )
            ]
            for item in REGISTRATION
        ]
    )

class ProductsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


# def get_name_by_id(order_list, target_id):
#     for item in order_list:
#         if item.get('id') == target_id:
#             return item.get('name')
#     return None  # Return None if the id is not found
    

