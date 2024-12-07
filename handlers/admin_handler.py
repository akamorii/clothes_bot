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

from db_bot.database import db_show, select_row_from_db, select_ids_from_db, add_order_to_db, count_update_db, order_update_db, add_clothes_db, delete_item_from_db, select_not_delivered_orders, select_sized_data_from_db, select_item_data_from_db, select_counts_from_db,select_all_from_table
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
    
    
class CheckOrderState(StatesGroup):
    show_orders = State()
    waiting_for_id = State()
    show_order = State()
   
    
class Update_count_state(StatesGroup):
    action_uptade_count = State()
    take_color_state = State()
    take_size_state = State()
    input_count = State()
    data_count = State()
    

add_action_kb = ReplyKeyboardBuilder()

add_action_kb.row(
    types.KeyboardButton(text="добавить"),
    types.KeyboardButton(text="удалить"),
)
add_action_kb.row(types.KeyboardButton(text="главное меню"))

# Клавиатура для выбора действия
edit_order_kb = ReplyKeyboardBuilder()
edit_order_kb.row(
    types.KeyboardButton(text="Добавить трек-номер"),
    types.KeyboardButton(text="Обновить статус"),
)
edit_order_kb.row(types.KeyboardButton(text="главное меню"))


edit_count_kb = ReplyKeyboardBuilder()

edit_count_kb.row(types.KeyboardButton(text="количество товара"))
edit_count_kb.row(
    types.KeyboardButton(text="добавить количество"),
    types.KeyboardButton(text="уменьшить количество"),
)
edit_count_kb.row(types.KeyboardButton(text="главное меню"))

# Обработчик команды "админ панель"
# Обработчик команды "админ панель"
@router.message(F.text == "админ панель")
async def admin_panel_show(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_ID:
        await state.set_state(AdminState.admin)
        await message.answer("Вы в админ панели. Выберите действие:", reply_markup=admin_keyboard)


    

@router.message(StateFilter(AdminState.admin), F.text == "изменить количество товара")
async def check_count(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    await state.clear()
    await state.set_state(Update_count_state.action_uptade_count)
    await message.answer(f"выберите пункт из меню", reply_markup=edit_count_kb.as_markup())
    

@router.message(StateFilter(Update_count_state.action_uptade_count), F.text == "количество товара")
async def show_count(message: types.Message, state: FSMContext):
    # await state.clear()
    # await state.set_state(Update_count_state.action_uptade_count)
    sized_items_table = await select_all_from_table("sizes_and_counts")
    items_table = await select_all_from_table("clothes")
    count_staff = await select_counts_from_db()
    
    response = []
    for sized_item_id, item_id, quantity in count_staff:
    # Находим информацию о размере и товаре
        sized_item = next((x for x in sized_items_table if x[0] == sized_item_id), None)
        item = next((x for x in items_table if x[0] == item_id), None)

        if sized_item and item:
            size = sized_item[1]
            color = item[3]
            response.append(f"{color} {size} - {quantity}")

# Формирование строки ответа
    response_message = "\n".join(response)
    
    await message.answer(f"{response_message}", reply_markup=edit_count_kb.as_markup())
    

@router.message(StateFilter(Update_count_state.action_uptade_count), F.text == "добавить количество" or F.text == "уменьшить количество")
async def add_count(message: types.Message, state: FSMContext):
    await message.answer(f"введите одежду в формате коллекция-цвет-размер-количество которое хотите добавить или уменьшить")
    await state.set_state(Update_count_state.data_count)
    action = message.text
    
    if action == "добавить количество":
        action = '+'
    elif action == "уменьшить количество":
        action = '-'
    else: 
        await state.clear()
        return
    
    await state.update_data(action = action)
    
@router.message(StateFilter(Update_count_state.data_count))
async def add_count_to(message: types.Message, state: FSMContext):
    
    try:
        data = (message.text).split('-')
        item_id = await select_ids_from_db('id', 'clothes', 'color', data[1], 'collection', data[0])
        sized_item_id =  await select_ids_from_db('sized_item_id', 'sizes_and_counts', 'size', data[2], 'item_id', item_id[0][0])
        
        data_state = await state.get_data()
        action = data_state.get('action')
        await count_update_db(action, data[3], sized_item_id[0][0])
            
    except Exception as e:
        print(e)
        await message.answer("попробуйте еще раз")
        await state.clear()
        await state.set_state(AdminState.admin)
        return
        # [collection, color, size, count]


    
    # await state.set_state(Update_count_state.data_count)


# @router.message(StateFilter(Update_count_state.action_uptade_count), F.text == "добавить количество")
# async def take_action_for_change_count_increase(message: types.Message, state: FSMContext):
#     await state.update_data(action = добавить)
#     await state.set_state(Update_count_state.take_color_state)
#     await message.answer(f"выберите колекцию количество которого хотите поменять")
#     # await state.clear()
    
    
# @router.message(StateFilter(AdminState.admin), F.text == '')
# async def admin_state_handler(message: types.Message, state: FSMContext):
#     await message.answer("Вы вернулись в главное меню.", reply_markup=admin_keyboard)


@router.message(StateFilter(Update_count_state.take_color_state))
async def take_collection_for_change_count(message: types.Message, state: FSMContext):
    await state.update_data(collection = message.text)
    await state.set_state(Update_count_state.take_color_state)
    await message.answer(f"выберите цвет количество которого хотите поменять")
    # await state.clear()
    
    
@router.message(StateFilter(Update_count_state.take_color_state))
async def take_color_for_change_Count(message: types.Message, state: FSMContext):
    await state.update_data(collection = message.text)
    await state.set_state(Update_count_state.take_color_state)
    await message.answer(f"выберите цвет количество которого хотите поменять")
    # await state.clear()
    


#TODO сделать функцию для просмотра не полученых заказов

@router.message(StateFilter(AdminState.admin), F.text == "посмотреть текущие заказы")
async def check_orders(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    await state.clear()
    await state.set_state(CheckOrderState.waiting_for_id)
    orders = await select_not_delivered_orders()
    res = [[i[0],i[4]] for i in orders]
    # orders_arr = []
    message_text = "\n".join([f"Заказ: {item[0]}. Статус: {item[4]}" for item in orders])    
    # result = {item[0]: item[4] for item in orders}
    state.update_data(waiting_for_id = orders)
    await message.answer(f"{message_text}\n\nесли вам хотите увидеть всю информацию о заказе введите его номер")


@router.message(StateFilter(CheckOrderState.waiting_for_id))
async def Check_order(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    order_id = message.text
    # data = await state.get_data()
    orders = await select_not_delivered_orders()
    # orders = orders[0]
    # orders = data.get("waiting_for_id")
    sized_data = await select_sized_data_from_db(order_id)
    sized_data = sized_data[0]
    
    item_data = await select_item_data_from_db(sized_data[0])
    item_data = item_data[0]
    
    await message.answer(
        f"информация о заказе {order_id}\n\n"
        # f"item_id: {orders}\n"
        f"Коллекция: {item_data[0]}\n"
        f"Цвет: {item_data[1]}\n"
        f"Размер: {sized_data[1]}\n"
        # f"sized_item_id: {sized_it_id}\n"
        f"Адрес: {orders[int(order_id)-1][3]}\n"
        f"user_id: {orders[int(order_id)-1][2]}\n"
        f"status: {orders[int(order_id)-1][4]}\n"
        f"track-num: {orders[int(order_id)-1][5]}\n"
    )
    
    await state.clear()
    await state.set_state(AdminState.admin)
    
    return

@router.message(StateFilter(AdminState.admin), F.text == "действия с товарами")
async def action_with_item(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    await state.clear()
    await state.set_state(AddItemState.action)
    await message.answer("вы хотите добавить или удалить товар?", reply_markup=add_action_kb.as_markup(resize_keyboard=True))
    
    
@router.message(StateFilter(AddItemState.action))
async def select_item_collection(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    action = message.text
    await state.update_data(action=action)
    await state.set_state(AddItemState.collection)
    await message.answer("введите название коллекции")
    
    
@router.message(StateFilter(AddItemState.collection))
async def select_item_collection(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    action = message.text
    await state.update_data(collection=action)
    await state.set_state(AddItemState.color)
    await message.answer("введите цвет")
    

@router.message(StateFilter(AddItemState.color))
async def select_item_collection(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
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
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    await state.set_state(AdminState.edit_order)
    await message.answer("Выберите действие для редактирования:", reply_markup=edit_order_kb.as_markup(resize_keyboard=True))


################

# Обработчик выбора действия с заказом
@router.message(StateFilter(AdminState.edit_order))
async def handle_edit_action(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    action = message.text
    if action in {"Редактировать пользовательские данные", "Добавить трек-номер", "Обновить статус"}:
        # Сохраняем выбранное действие
        # await state.update_data(action=action)
        await state.set_state(AdminState.waiting_for_order_id)
        await state.update_data(action=action)
        await message.answer("Введите номер заказа, который хотите обработать:")
    elif action == "Вернуться в главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=admin_keyboard)
    else:
        await message.answer("Выберите действие из предложенных на клавиатуре.")



# Обработчик ввода номера заказа
@router.message(StateFilter(AdminState.waiting_for_order_id))
async def process_order_id(message: types.Message, state: FSMContext):
    if message.text == "главное меню":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_keyboard)
        return
    order_id = message.text
    if not order_id.isdigit():
        await message.answer("Пожалуйста, введите корректный номер заказа.")
        await state.clear()
        return

    # Сохраняем номер заказа
    await state.update_data(order_id=order_id)

    # Получаем выбранное действие из состояния
    data = await state.get_data()
    action = data.get("action")
    # order_id = data.get("order_id")

    if action == "Добавить трек-номер":
        await state.set_state(AdminState.waiting_for_tracking_number)
        await message.answer("Введите трек-номер для заказа:")
    elif action == "Обновить статус":
        await state.set_state(AdminState.waiting_for_status_update)
        await message.answer("Введите новый статус для заказа:")
    else:
        await state.clear()
        await message.answer("где-то произошла ошибка")

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
 
    
