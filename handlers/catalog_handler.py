from aiogram import types, Router
from aiogram.types import KeyboardButton
from aiogram.filters import Command
from handlers.keyboards import main_keyboard
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db_bot.database import db_show, select_row_from_db

# Создаем роутер
router = Router()

# создание машины состояний
class Make_order(StatesGroup):
    collection = State()
    color = State()
    size = State()
    addr = State()
    


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
    # Отправляем сообщение с клавиатурой
    await message.answer(
        "Выберите коллекцию:",
        reply_markup=catalog_kb.as_markup(resize_keyboard=True)  # Обязательно вызываем as_markup()
    )


@router.message(Make_order.collection)
async def make_order(message: types.Message, state: FSMContext):
    await state.update_data(collection = message.text)
    await state.set_state(Make_order.color)
    tuple_list = await db_show(['color'], 'clothes')
    # Извлекаем уникальные элементы из результата
    unique_elements = list({item[0] for item in tuple_list})
    # Создаем клавиатуру
    catalog_kb2 = ReplyKeyboardBuilder()
    
    for el in unique_elements:
        catalog_kb2.add(KeyboardButton(text=el))
        
    await message.answer('введите цвет', reply_markup=catalog_kb2.as_markup(resize_keyboard=True))


@router.message(Make_order.color)
async def make_order_two(message: types.Message, state: FSMContext):
    await state.update_data(color = message.text)
    await state.set_state(Make_order.size)
    tuple_list = await db_show(['size'], 'sizes_and_counts', eq1='count')
    # Извлекаем уникальные элементы из результата
    unique_elements = list({item[0] for item in tuple_list})
    # Создаем клавиатуру
    catalog_kb = ReplyKeyboardBuilder()
    for el in unique_elements:
        catalog_kb.add(KeyboardButton(text=str(el)))
        
    await message.answer('размер', reply_markup=catalog_kb.as_markup(resize_keyboard=True))
    

@router.message(Make_order.size)
async def make_order_three(message: types.Message, state: FSMContext):
    await state.update_data(size = message.text)
    await state.set_state(Make_order.addr)
    
    await message.answer("Введите адрес пункта Почты России 🚛 Например: Московская область, улица Пушкина, дом 37")
    
    
@router.message(Make_order.addr)
async def make_order_four(message: types.Message, state: FSMContext):
    await state.update_data(addr = message.text)
    data = await state.get_data()
    
    await message.answer(f"вы сделали заказ... {data}")
    await state.clear()
    
