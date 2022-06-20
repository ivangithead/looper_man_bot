from aiogram import executor
import logging
###############################
from main import dp, on_startup
from handlers import *
from callback import *
import middlewares
import sqlite

logger = logging.getLogger("bot.loader")

if __name__ == "__main__":
	middlewares.setup(dp)
	logger.info("Бот запущен.")
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)