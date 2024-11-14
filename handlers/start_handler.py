from aiogram import types, Router
from aiogram.filters import Command
from handlers.keyboards import main_keyboard, main_admin_keyboard
from vars import ADMIN_ID
# Создаем роутер
router = Router()

# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(f"""✨Здравствуйте! Вас приветствует компания Raven.
                         
Оформления заказа - кнопка 1(кнопка 1).
Тех. поддержка – кнопка 2(кнопка 2).
Наши соцсети – кнопка 3 (кнопка 3)
"""
                        , reply_markup=main_keyboard )
    print(message.from_user.id)
    if message.from_user.id in ADMIN_ID:
        await message.answer(f"вы вошли как админ!", reply_markup=main_admin_keyboard )