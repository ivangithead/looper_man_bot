from aiogram import types
from main import dp, bot

@dp.my_chat_member_handler()
async def my_chat_member(message: types.Message) -> None:
	await bot.leave_chat(message.chat.id)