from aiogram import types, Router
from aiogram.filters import Command

mkb = [
        [types.KeyboardButton(text="корзина")],
        [types.KeyboardButton(text="каталог")],
        [types.KeyboardButton(text="контакты")]
]

makb = [
        [types.KeyboardButton(text="корзина")],
        [types.KeyboardButton(text="каталог")],
        [types.KeyboardButton(text="контакты")],
        [types.KeyboardButton(text="админ панель")]
]

adkb = [
        [types.KeyboardButton(text="редактировать заказ")],
        [types.KeyboardButton(text="добавить коллекцию")],
        [types.KeyboardButton(text="добавить товар")],
        [types.KeyboardButton(text="главное меню")]
]

main_keyboard = types.ReplyKeyboardMarkup(keyboard=mkb)

main_admin_keyboard = types.ReplyKeyboardMarkup(keyboard=makb)

admin_keyboard = types.ReplyKeyboardMarkup(keyboard=adkb)