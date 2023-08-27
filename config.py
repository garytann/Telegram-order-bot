from telebot import types
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter


MENU = [
    {'id': '0', 'name': 'Order',},
    {'id': '1', 'name': 'Check Order Status'},
    {'id': '2', 'name': 'Cancel Order'},
    {'id': '3', 'name': 'Update Address'},
    {'id': '4', 'name': 'Exit'}
]

ORDER = [
    {'id': '0', 'name': 'Option 1',},
    {'id': '1', 'name': 'Option 2'},
]

REGISTRATION = [
    {'id': '0', 'name': 'Register',},
]


register_factory = CallbackData('register_id', prefix='register')
order_factory = CallbackData('order_id', prefix='order')
menu_factory = CallbackData('menu_id', prefix='menu')

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

    

