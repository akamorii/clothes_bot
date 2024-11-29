from aiogram import types, Router
from aiogram.types import KeyboardButton
from aiogram.filters import Command
from handlers.keyboards import main_keyboard, main_admin_keyboard
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from handlers.payment import make_payment, get_payment_status
from bot_instance import bot

from vars import ADMIN_ID, CHAT_ID

import time

import asyncio

from db_bot.database import db_show, select_row_from_db, select_ids_from_db, add_order_to_db, count_update_db, select_all_from_table, select_by_one_select

router = Router()
class MyОrderState(StatesGroup):
    select_orders = State()
    select_one_order = State()
    
  
@router.message(F.text == "тех. поддержка")
async def check_my_orders(message: types.Message, state: FSMContext):