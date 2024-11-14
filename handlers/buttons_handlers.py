from aiogram import types, Router
from aiogram.filters import Command, Text
from handlers.keyboards import main_keyboard, main_admin_keyboard
from vars import ADMIN_ID
# from aiogram.filters import Text

router = Router()

@router.message(Text("каталог"))
async def show_catalog (message: types.Message):
    await message.answer(f"hello {message.from_user.first_name}")