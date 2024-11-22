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

from vars import ADMIN_ID

import time

import asyncio

from db_bot.database import db_show, select_row_from_db, select_ids_from_db, add_order_to_db, count_update_db

# from yookassa import Payment

# Создаем роутер
router = Router()

# создание машины состояний
class Make_order(StatesGroup):
    collection = State()
    color = State()
    size = State()
    addr = State()
    confirm_order = State()
    
confirm_order_inline_kb = [
        [types.InlineKeyboardButton(text="оплатить заказ", callback_data='confirm_order')],
        [types.InlineKeyboardButton(text="отменить и вернутся в главное меню", callback_data='cancel_order')]
]

@router.message(F.text == "каталог")
async def handle_catalog(message: types.Message, state: FSMContext):
    await state.set_state(Make_order.collection)
    
    # Получаем данные из БД асинхронно
    tuple_list = await db_show(['collection'], 'clothes')
    # Извлекаем уникальные элементы из результата
    unique_elements = list({item[0] for item in tuple_list})
    # Создаем клавиатуру
    catalog_kb = ReplyKeyboardBuilder()
    for el in unique_elements:
        catalog_kb.add(KeyboardButton(text=el))
        
    catalog_kb.row(types.KeyboardButton(text="главное меню"))
    # Отправляем сообщение с клавиатурой
    await message.answer(
        "Выберите коллекцию:",
        reply_markup=catalog_kb.as_markup(resize_keyboard=True)  # Обязательно вызываем as_markup()
    )


@router.message(Make_order.collection)
async def make_order(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    await state.update_data(collection = message.text)
    await state.set_state(Make_order.color)
    tuple_list = await db_show(['color'], 'clothes')
    # Извлекаем уникальные элементы из результата
    unique_elements = list({item[0] for item in tuple_list})
    # Создаем клавиатуру
    catalog_kb2 = ReplyKeyboardBuilder()
    
    for el in unique_elements:
        catalog_kb2.add(KeyboardButton(text=el))
    catalog_kb2.row(types.KeyboardButton(text="главное меню"))
    
    await message.answer('введите цвет', reply_markup=catalog_kb2.as_markup(resize_keyboard=True))


@router.message(Make_order.color)
async def make_order_two(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    await state.update_data(color = message.text)
    await state.set_state(Make_order.size)
    tuple_list = await db_show(['size'], 'sizes_and_counts', eq1='count')
    # Извлекаем уникальные элементы из результата
    unique_elements = list({item[0] for item in tuple_list})
    unique_elements = sorted(unique_elements)
    # Создаем клавиатуру
    catalog_kb = ReplyKeyboardBuilder()
    for el in unique_elements:
        catalog_kb.add(KeyboardButton(text=str(el)))
    catalog_kb.row(types.KeyboardButton(text="главное меню"))
        
    await message.answer('размер', reply_markup=catalog_kb.as_markup(resize_keyboard=True))
    

@router.message(Make_order.size)
async def make_order_three(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    await state.update_data(size = message.text)
    await state.set_state(Make_order.addr)
    main_menu = ReplyKeyboardBuilder()
    main_menu.row(types.KeyboardButton(text="главное меню"))
    await message.answer("Введите адрес пункта Почты России 🚛 Например: Московская область, улица Пушкина, дом 37", reply_markup=main_menu.as_markup())
    
    
@router.message(Make_order.addr)
async def make_order_four(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    await state.update_data(addr = [message.text, message.from_user.id])
    
    data = await state.get_data()
    
    await state.set_state(Make_order.confirm_order)
    
    await message.answer(f"вы сделали заказ...", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=confirm_order_inline_kb))
    # await state.clear()
    
    
@router.callback_query(StateFilter(Make_order.confirm_order), F.data == 'confirm_order')
async def confirm_order_callback(callback: types.CallbackQuery, state: FSMContext):
    # Получаем данные из состояния
    data = await state.get_data()
    collection = data.get('collection')
    color = data.get('color')
    size = data.get('size')
    addr = data.get('addr')[0]
    user_id = data.get('addr')[1] 
    
    payment_data = await (make_payment(100.0))
    
    payment_url = payment_data['confirmation']['confirmation_url']
    payment_id = payment_data['id']
    
    time.sleep(1)
    
    inline_button_for_pay = [
        [types.InlineKeyboardButton(text='оплатить', url=payment_url)]
    ]
    
    await callback.message.answer('вот ваша ссылка для оплаты',reply_markup=types.InlineKeyboardMarkup(inline_keyboard=inline_button_for_pay))

    while True:
        payment_status = await get_payment_status(payment_id)  # Асинхронная операция
        if payment_status['paid'] == True:
            print("Оплата подтверждена!")
            break
        await asyncio.sleep(10)  # Асинхронная пауза

    it_id = await select_ids_from_db('id', 'clothes', 'color', color, 'collection', collection)
    
    sized_it_id = await select_ids_from_db('sized_item_id', 'sizes_and_counts', 'item_id', it_id[0][0], 'size', size)
    
    await callback.message.answer(
        f"Ваш заказ подтвержден!\n\n"
        # f"item_id: {it_id}\n"
        f"Коллекция: {collection}\n"
        f"Цвет: {color}\n"
        f"Размер: {size}\n"
        # f"sized_item_id: {sized_it_id}\n"
        f"Адрес: {addr}\n"
        # f"user_id: {user_id}"
    )
    
    # TODO
    
    await add_order_to_db(sized_it_id[0][0], user_id, addr)
    
    await count_update_db('-', 1, 1)
    
    order_id = await select_row_from_db('orders', 'user_id', user_id)
    # print(order_id)
    await callback.message.answer(f"ваш номер заказа {order_id[-1][0]}")
    
    # Завершаем состояние
    await state.clear()
    # await callback.answer()  # Закрываем всплывающее уведомление Telegram

# Хэндлер для отмены заказа
@router.callback_query(StateFilter(Make_order.confirm_order), F.data == 'cancel_order')
async def cancel_order_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id in ADMIN_ID:
        await callback.message.answer(f"Заказ отменен. Возвращаюсь в главное меню.", reply_markup=main_admin_keyboard )
    else:
        await callback.message.answer("Заказ отменен. Возвращаюсь в главное меню.", reply_markup=main_keyboard)
    # Завершаем состояние
    await state.clear()
    # await callback.answer()  # Закрываем всплывающее уведомление Telegram
