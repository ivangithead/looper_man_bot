from aiogram import types
import time
import logging
#######################################
from main import dp, bot
from data import BOT_AUTHOR, RATE_LIMIT
from keyboards import *
from utils import rate_limit
from unix import unix_to_date
import sqlite

logger = logging.getLogger("bot.handlers.commands.start")

@rate_limit(limit=RATE_LIMIT)
@dp.message_handler(commands=["start"])
async def start(message: types.Message) -> None:
	try:
		name = message.from_user.first_name.title()

		if sqlite.user_already_exists(message.from_user.id):
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

			await message.answer(f"Привет, <b><i>{name}</i></b>! Я тебя помню, вот твой профиль:\n\n\
👤 <b>Профиль id{message.from_user.id}</b>\n\
├ <b>Получено сэмплов</b>: {samples}\n\
├ <b>Первое сообщение боту</b>: {registration}\n\
└ <b>Подписка</b>: {subscribe}",
				reply_markup=general_markup)

		else:
			await bot.send_photo(
				message.chat.id,
				"https://i.postimg.cc/rpzVt1v0/help.jpg",
				caption=f"Привет, <b><i>{name}</i></b>!\nЭтот бот поможет тебе в создании музыки. \n\n\
<b>Как пользоваться ботом?</b>\n\n\
Всё предельно просто, ты будешь получать все новые сэмплы автоматически. Как только на сайте <i>looperman.com</i> выходит сэмпл - он сразу же отправляется тебе!\n\
Это позволит тебе <b>первым</b> создавать и отправлять сочные биты исполнителям.\n\
Скачать вы его сможете <b>прямо в телеграме</b>, либо нажав на кнопку \"<b>Скачать</b> ⬇️\".\n\n\
<i>Я выдал тебе двухдневный пробный период для ознакомления!</i>",
				reply_markup=general_markup
			)

			sqlite.register_user(
				message.from_user.id, 
				message.from_user.username, 
				message.from_user.first_name,
				message.from_user.last_name
			)
	except Exception as ex:
		logger.critical(ex)