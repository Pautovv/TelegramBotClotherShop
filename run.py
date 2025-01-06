import os
import asyncio 
import logging
from dotenv import load_dotenv
from app.handlers import router
from app.admin import admin
from aiogram import Bot, Dispatcher
from app.data.models import async_main

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

async def main():
    await async_main()
    load_dotenv()
    dp.include_routers(admin, router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')