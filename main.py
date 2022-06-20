import logging
import logging.handlers
import asyncio
############################################################
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram import types
from data import TOKEN, LOGGER_FORMAT
from threads import main_thread

storage = MemoryStorage()
bot     = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp      = Dispatcher(bot, storage=storage)

def init_new_logger(name: str) -> logging.Logger:
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)

	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
	stream_handler.setLevel(logging.DEBUG)

	file_handler = logging.handlers.RotatingFileHandler(filename="logs/log.log")
	file_handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
	file_handler.setLevel(logging.DEBUG)

	logger.addHandler(file_handler)
	logger.addHandler(stream_handler)
	logger.info("Корневой логгер инициализирован.")

init_new_logger("bot")

async def on_startup(x):
	asyncio.create_task(main_thread(bot))