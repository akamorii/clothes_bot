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
    
  
@router.message(F.text == "мои заказы")
async def check_my_orders(message: types.Message, state: FSMContext):
    
    sizes_and_counts = await select_all_from_table("sizes_and_counts")
    
    items = await select_all_from_table('clothes')
    
    try:
        orders = await select_by_one_select(message.from_user.id, 'user_id', 'orders')
        
    except Exception as e:
        print(e)
        await message.answer('у вас нет заказов')
        await state.clear()
        return
    
    
    # time.sleep(2)
    # zxc = 123
    item_dict = {item[0]: item for item in items}
    sizes_dict = {size[0]: size for size in sizes_and_counts}

    # Создаем список сообщений для каждого заказа
    messages = []
        
    for order in orders:
        order_id, sized_item_id, user_id, address, status, track_num = order

        # Получаем данные о размере и товаре
        size_data = sizes_dict.get(sized_item_id)
        if not size_data:
            messages.append(f"Номер заказа {order_id}: данные о размере не найдены")
            continue

        size, count, item_id = size_data[1], size_data[2], size_data[3]
        item_data = item_dict.get(item_id)
        if not item_data:
            messages.append(f"Номер заказа {order_id}: данные о товаре не найдены")
            continue

        collection, item_type, color = item_data[1], item_data[2], item_data[3]

        # Формируем сообщение о заказе
        message_res = (
            f"Номер заказа: {order_id}\n"
            f"Цвет: {color}\n"
            f"Размер: {size}\n"
            f"Тип: {item_type}\n"
            f"Коллекция: {collection}\n"
            f"Статус: {status}\n"
            f"Адрес: {address}\n"
            f"Трек-номер: {track_num}\n"
            # f"Остаток на складе: {count if count > 0 else 'Нет в наличии'}"
        )
        messages.append(message_res)
    try:
        # print(zxc)
        if not messages:
            raise Exception("нет заказов")
        
    except Exception as e:
        await state.clear()
        await message.answer(str(e))
        return

    res = "Если Вы не уверены в правильности написания адреса пункта выдачи, после оплаты заказа напишите в @Business228777 и напишите номер своего заказа и адрес пункта выдачи. Мы все проверим и отправим именно туда, куда Вам надо🤝\n\n".join(messages)
    
    await message.answer(res)


 