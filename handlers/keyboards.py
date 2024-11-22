from aiogram import types, Router
from aiogram.filters import Command

mkb = [
        [types.KeyboardButton(text="каталог")],
        [types.KeyboardButton(text="наши соц-сети")],
        [types.KeyboardButton(text="тех. поддержка")],
        [types.KeyboardButton(text="мои заказы")],
]

makb = [
        [types.KeyboardButton(text="каталог")],
        [types.KeyboardButton(text="наши соц-сети")],
        [types.KeyboardButton(text="тех. поддержка")],
        [types.KeyboardButton(text="мои заказы")],
        [types.KeyboardButton(text="админ панель")]
]

adkb = [
        [types.KeyboardButton(text="редактировать заказ")],
        [types.KeyboardButton(text="действия с товарами")],
        [types.KeyboardButton(text="посмотреть текущие заказы")],
        [types.KeyboardButton(text="изменить количество товара")],
        [types.KeyboardButton(text="главное меню")]
]

# confirm_order_inline_kb = [
#         [types.inline_keyboard_button(text="подтвердить заказ", )]
# ]

main_keyboard = types.ReplyKeyboardMarkup(keyboard=mkb, input_field_placeholder='выберите пункт в меню', resize_keyboard=True)

main_admin_keyboard = types.ReplyKeyboardMarkup(keyboard=makb, input_field_placeholder='выберите пункт в меню', resize_keyboard=True)

admin_keyboard = types.ReplyKeyboardMarkup(keyboard=adkb, input_field_placeholder='выберите пункт в меню', resize_keyboard=True)