from aiogram import types, Router
from aiogram.filters import Command
from handlers.keyboards import main_keyboard
from aiogram import F
import asyncio

import sys
# sys.path.append('../')

from db_bot.database import db_show

from handlers.keyboards import admin_keyboard
# Создаем роутер

router = Router()

rows = asyncio.run(db_show(['collection'], 'clothes'))

# Обработчик команды /dice
@router.message(F.text == "админ панель")
async def handle_help(message: types.Message):
    await message.answer(f"{tuple(rows)}админ панель", reply_markup=admin_keyboard)