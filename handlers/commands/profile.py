from aiogram import types
import time
import logging
#############################
from main import dp
from data import RATE_LIMIT
from unix import unix_to_date
from utils import rate_limit
import sqlite

logger = logging.getLogger("bot.handlers.commands.profile")

@rate_limit(limit=RATE_LIMIT)
@dp.message_handler(commands=["profile", "профиль"])
async def profile(message: types.Message) -> None:
	try:
		samples        = sqlite.get_user_samples(message.from_user.id)
		subscribe_time = sqlite.get_user_subtime(message.from_user.id)
		subscribe_date = unix_to_date(subscribe_time)
		registration   = unix_to_date(sqlite.get_user_registration(message.from_user.id))
			
		time_now = int(time.time())

		if subscribe_time == 0:
			subscribe = "Безлимит 🎵⚡️"
		elif subscribe_time > time_now:
			subscribe = f"до {subscribe_date}"
		elif subscribe_time < time_now or \
			 subscribe_time == time_now:
			subscribe = f"истекла {subscribe_date}"

		await message.answer(f"👤 <b>Профиль id{message.from_user.id}</b>\n\
├ <b>Получено сэмплов</b>: {samples}\n\
├ <b>Первое сообщение боту</b>: {registration}\n\
└ <b>Подписка</b>: {subscribe}")
	except Exception as ex:
		logger.warning(ex)
