from aiogram import types
from main import dp

@dp.message_handler(commands=["filter", "фильтр"])
async def filter(message: types.Message) -> None:
	await message.reply("<b>В разработке.</b>")
