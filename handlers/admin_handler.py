from aiogram import types, Router
from aiogram.types import KeyboardButton
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
# from handlers.payment import make_payment, get_payment_status

from handlers.keyboards import main_keyboard, main_admin_keyboard, admin_keyboard

from vars import ADMIN_ID

import time

import asyncio

from db_bot.database import db_show, select_row_from_db, select_ids_from_db, add_order_to_db, count_update_db, order_update_db, add_clothes_db, delete_item_from_db
# Создаем роутер

router = Router()
    
# Состояния
class AdminState(StatesGroup):
    admin = State()
    edit_order = State()
    waiting_for_order_id = State()
    waiting_for_tracking_number = State()
    waiting_for_status_update = State()

class AddItemState(StatesGroup):
    action = State()
    collection = State()
    # item_name = State()
    color = State()

add_action_kb = ReplyKeyboardBuilder()

add_action_kb.row(
    types.KeyboardButton(text="добавить"),
    types.KeyboardButton(text="удалить"),
)
add_action_kb.row(types.KeyboardButton(text="Вернуться в главное меню"))

# Клавиатура для выбора действия
edit_order_kb = ReplyKeyboardBuilder()
edit_order_kb.row(
    types.KeyboardButton(text="Добавить трек-номер"),
    types.KeyboardButton(text="Обновить статус"),
)
edit_order_kb.row(types.KeyboardButton(text="Вернуться в главное меню"))

# Обработчик команды "админ панель"
# Обработчик команды "админ панель"
@router.message(F.text == "админ панель")
async def admin_panel_show(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_ID:
        await state.set_state(AdminState.admin)
        await message.answer("Вы в админ панели. Выберите действие:", reply_markup=admin_keyboard)


#TODO сделать функцию для просмотра не полученых заказов


@router.message(StateFilter(AdminState.admin), F.text == "действия с товарами")
async def action_with_item(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddItemState.action)
    await message.answer("вы хотите добавить или удалить товар?", reply_markup=add_action_kb.as_markup(resize_keyboard=True))
    
    
@router.message(StateFilter(AddItemState.action))
async def select_item_collection(message: types.Message, state: FSMContext):
    action = message.text
    await state.update_data(action=action)
    await state.set_state(AddItemState.collection)
    await message.answer("введите название коллекции")
    
    
@router.message(StateFilter(AddItemState.collection))
async def select_item_collection(message: types.Message, state: FSMContext):
    action = message.text
    await state.update_data(collection=action)
    await state.set_state(AddItemState.color)
    await message.answer("введите цвет")
    

@router.message(StateFilter(AddItemState.color))
async def select_item_collection(message: types.Message, state: FSMContext):
    action = message.text
    await state.update_data(color=action)
    # await state.set_state(AddItemState.collection)
    data = await state.get_data()
    collection = data.get('collection')
    color = data.get('color')
    action = data.get('action')
    
    if action == "добавить":
        await add_clothes_db('clothes', collection, 't_shirt', color)
    elif action == "удалить":
        await delete_item_from_db(collection=collection, color=color)
    else:
        await message.answer("вы некоректно ввели действие")
        return
    
    await state.clear()
    
    await message.answer(f"вы уcпешно {action} {color} футболку из {collection}")


# Обработчик выбора "Редактировать заказ"
@router.message(StateFilter(AdminState.admin), F.text == "редактировать заказ")
async def edit_orders_panel(message: types.Message, state: FSMContext):
    await state.set_state(AdminState.edit_order)
    await message.answer("Выберите действие для редактирования:", reply_markup=edit_order_kb.as_markup(resize_keyboard=True))


################

# Обработчик выбора действия с заказом
@router.message(StateFilter(AdminState.edit_order))
async def handle_edit_action(message: types.Message, state: FSMContext):
    action = message.text
    if action in {"Редактировать пользовательские данные", "Добавить трек-номер", "Обновить статус"}:
        # Сохраняем выбранное действие
        # await state.update_data(action=action)
        await state.set_state(AdminState.waiting_for_order_id)
        await message.answer("Введите номер заказа, который хотите обработать:")
    elif action == "Вернуться в главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=admin_keyboard)
    else:
        await message.answer("Выберите действие из предложенных на клавиатуре.")


# Обработчик ввода номера заказа
# @router.message(StateFilter(AdminState.waiting_for_order_id))
# async def process_order_id(message: types.Message, state: FSMContext):
#     order_id = message.text
#     if not order_id.isdigit():
#         await message.answer("Пожалуйста, введите корректный номер заказа.")
#         return

#     # Сохраняем номер заказа
#     await state.update_data(order_id=order_id)

#     # Получаем выбранное действие из состояния
#     data = await state.get_data()
#     action = data.get("action")

#     if action == "Добавить трек-номер":
#         await message.answer(f"Добавление трек-номера для заказа {order_id}.")
#         # Здесь логика добавления трек-номера
#     elif action == "Обновить статус":
#         await message.answer(f"Обновление статуса для заказа {order_id}.")
#         # Здесь логика обновления статуса

#     # Возврат в главное меню
#     await state.set_state(AdminState.admin)
#     await message.answer("Выберите следующее действие или вернитесь в главное меню.", reply_markup=admin_keyboard)

#####################

# Обработчик ввода номера заказа
@router.message(StateFilter(AdminState.waiting_for_order_id))
async def process_order_id(message: types.Message, state: FSMContext):
    order_id = message.text
    if not order_id.isdigit():
        await message.answer("Пожалуйста, введите корректный номер заказа.")
        return

    # Сохраняем номер заказа
    await state.update_data(order_id=order_id)

    # Получаем выбранное действие из состояния
    data = await state.get_data()
    action = data.get("action")

    if action == "Добавить трек-номер":
        await state.set_state(AdminState.waiting_for_tracking_number)
        await message.answer("Введите трек-номер для заказа:")
    elif action == "Обновить статус":
        await state.set_state(AdminState.waiting_for_status_update)
        await message.answer("Введите новый статус для заказа:")


# Обработчик ввода трек-номера
@router.message(StateFilter(AdminState.waiting_for_tracking_number))
async def process_tracking_number(message: types.Message, state: FSMContext):
    tracking_number = message.text

    # Сохраняем трек-номер
    data = await state.get_data()
    order_id = data.get("order_id")

    # Здесь логика сохранения трек-номера в БД
    # Например:
    # await db.update_tracking_number(order_id, tracking_number)
    await order_update_db(mean=tracking_number, id=order_id, column="tracknum")


    await message.answer(f"Трек-номер {tracking_number} добавлен для заказа {order_id}.")

    # Возврат в главное меню
    await state.set_state(AdminState.admin)
    await message.answer("Выберите следующее действие или вернитесь в главное меню.", reply_markup=admin_keyboard)


# Обработчик ввода нового статуса
@router.message(StateFilter(AdminState.waiting_for_status_update))
async def process_status_update(message: types.Message, state: FSMContext):
    new_status = message.text

    # Сохраняем новый статус
    data = await state.get_data()
    order_id = data.get("order_id")

    # Здесь логика обновления статуса в БД
    # Например:
    # await db.update_order_status(order_id, new_status)
    await order_update_db(mean=new_status, id=order_id)

    await message.answer(f"Статус заказа {order_id} обновлен на: {new_status}.")

    # Возврат в главное меню
    await state.set_state(AdminState.admin)
    await message.answer("Выберите следующее действие или вернитесь в главное меню.", reply_markup=admin_keyboard)