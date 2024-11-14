from aiogram import types, Router
from aiogram.filters import Command
from handlers.keyboards import main_keyboard, main_admin_keyboard
from vars import ADMIN_ID

# Создаем роутер
router = Router()

# Обработчик команды /dice
@router.message()
async def any_hand(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer("я тебя не понимаю", reply_markup=main_admin_keyboard)
        return
    await message.answer("я тебя не понимаю", reply_markup=main_keyboard)