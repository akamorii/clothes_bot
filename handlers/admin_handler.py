from aiogram import types, Router
from aiogram.filters import Command
from handlers.keyboards import main_keyboard

# Создаем роутер
router = Router()

# Обработчик команды /dice
@router.message(text='')
async def roll_dice(message: types.Message):
    await message.answer("выберите цвет", reply_markup=main_keyboard)