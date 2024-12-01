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
    
  
@router.message(F.text == "наши соц-сети")
async def check_my_orders(message: types.Message, state: FSMContext):
    text = (
        "Привет! Вот ссылки на наши соцсети:\n\n"
        "[Telegram](https://t.me/raven_KMV) — Подписывайся на наш канал\n"
        "[VK](vk.com/club228341079) - мы в ВК\n"
        "[Instagram](https://www.instagram.com/raven_kmv/profilecard/?igsh=eHRlajk1aDFuMjl3) — Следи за новостями\n"
        "[YouTube](https://www.youtube.com/channel/UCcZ-FPPJ_DjK27jzfizMKFA) - наш канал на ютубе")
    await message.answer(text, parse_mode="Markdown")