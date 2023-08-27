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

class ProductsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)
    

