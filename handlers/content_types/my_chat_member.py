import logging
from aiogram import types
from main import dp, bot

logger = logging.getLogger("bot.handlers.content_types.my_chat_member")

@dp.my_chat_member_handler()
async def my_chat_member(message: types.Message) -> None:
	try:
		await bot.leave_chat(message.chat.id)
	except Exception as ex:
		logger.critical(ex)
