from aiogram import types, Router
from aiogram.filters import Command
from handlers.keyboards import main_keyboard
from aiogram import F

from handlers.keyboards import admin_keyboard
# Создаем роутер

router = Router()

# Обработчик команды /dice
@router.message(F.text == "админ панель")
async def handle_help(message: types.Message):
    await message.answer("zxc", reply_markup=admin_keyboard)