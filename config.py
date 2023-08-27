from telebot import types
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

bot_token = "6362946007:AAHamKb16t5Q-OTRQuyLyOoH_AXkiwaLa5M"

MENU = [
    {'id': '0', 'name': 'Order',},
    {'id': '1', 'name': 'Order Status'},
    {'id': '2', 'name': 'Cancel Order'},
    {'id': '3', 'name': 'Exit'}
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
    

