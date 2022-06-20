from aiogram import types
import time
import logging
######################################
from main import dp
from data import RATE_LIMIT
from keyboards import subscribe_markup
from unix import unix_to_date
from utils import rate_limit
import sqlite

logger = logging.getLogger("bot.handlers.commands.subscribe")

@rate_limit(limit=RATE_LIMIT)
@dp.message_handler(commands=["subscribe", "подписка", "sub"])
async def subscribe(message: types.Message) -> None:
	try:
		subscribe_time = sqlite.get_user_subtime(message.from_user.id)
		subscribe_date = unix_to_date(subscribe_time)
		markup = subscribe_markup

		time_now = int(time.time())

		if subscribe_time == 0:
			subscribe = "Безлимит 🎵⚡️"
			access_samples = "доступно"
			markup = types.InlineKeyboardMarkup() # Удаляем клавиатуру для юзера, купившего подписку навсегда

		elif subscribe_time > time_now:
			subscribe = f"<b>Активна до</b> {subscribe_date}"
			access_samples = "доступно"

		elif subscribe_time < time_now or \
			 subscribe_time == time_now:
			subscribe = f"<b>Истекла</b> {subscribe_date}"
			access_samples = "недоступно"

		await message.answer(
			f"<b>🎶 Подписка id{message.from_user.id}</b>\n├ <b>Получение сэмплов</b>: {access_samples}\n└ {subscribe}", 
			reply_markup=markup
			)
	except Exception as ex:
		logger.warning(ex)