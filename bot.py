import logging
import asyncio

from aiogram import Bot, Dispatcher, types, Router
# from aiogram.utils import executor
from aiogram.filters import Command
from aiogram import F
from aiogram.types import Message

from handlers.start_handler import router as start_router
from handlers.dice_handler import router as dice_router
from handlers.admin_handler import router as admin_router
from handlers.any_handler import router as any_router
from handlers.catalog_handler import router as catalog_router
# from handlers.dice_handler import router as dice_router
# from handlers.buttons_handlers import router as btns_router

import os

from vars import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()
# router = Router()
# dp.include_router(router)

# @router.message(F.text == "hello")
# async def handle_help(message: Message):
#     await message.answer("zxc")
# register_start_handler(dp)
# dp.include_router(dice_router)
dp.include_router(catalog_router)
dp.include_router(start_router)
dp.include_router(dice_router)
dp.include_router(admin_router)

dp.include_router(any_router)
# dp.include_router(btns_router)
# @router.message(Command(commands=['start']))
# async def echo(message: types.Message):
#     await message.answer(text='message')


    
    
    
async def main ():
    await dp.start_polling(bot, skip_updates=False)
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())