from aiogram import types, Router, F
from aiogram.filters import Command
from handlers.keyboards import main_keyboard, main_admin_keyboard
from vars import ADMIN_ID
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

# Создаем роутер
router = Router()

# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: types.Message):
    print(message.from_user.id)
    await message.answer(f"""✨Здравствуйте! Вас приветствует компания Raven.
                         
Оформления заказа - кнопка 1(кнопка 1).
Тех. поддержка – кнопка 2(кнопка 2).
Наши соцсети – кнопка 3 (кнопка 3)
"""
                        , reply_markup=main_keyboard )
    print(message.from_user.id)
    if message.from_user.id in ADMIN_ID:
        await message.answer(f"вы вошли как админ!", reply_markup=main_admin_keyboard )
        
@router.message(StateFilter(None), F.text == "главное меню")
async def retunr_to_menu(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_ID:
        await message.answer(f"вы вернулись в главное меню", reply_markup=main_admin_keyboard )
        await state.clear()
        return
    await state.clear()
    await message.answer(f"вы вернулись в главное меню", reply_markup=main_keyboard )