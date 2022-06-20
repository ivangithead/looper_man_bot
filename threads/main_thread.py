import asyncio
import logging
#################################################
from aiogram import Bot
from aiogram import types
from parser import get_loops_count, get_last_loop
import sqlite

logger = logging.getLogger("bot.threads.main_thread")

async def main_thread(bot: Bot) -> None:
	while True:
		try:
			loops_count1 = get_loops_count()

			while True:
				loops_count2 = get_loops_count()

				if loops_count2 > loops_count1:
					last_loop = get_last_loop()

					caption = f"🎹 <b><a href='{last_loop[3]}'>{last_loop[2]}</a></b> — \
	<b>{last_loop[1]}</b>\n\
	├ <b>BPM</b>: {last_loop[5].split()[0]}\n\
	├ <b>Длительность</b>: {last_loop[4].strip()}\n\
	├ <b>Жанр</b>: {last_loop[6].strip()}\n\
	├ <b>Категория</b>: {last_loop[7].strip()}\n\
	└ <b>Тональность</b>: {last_loop[10].split(':')[-1].strip()}"
					
					markup = types.InlineKeyboardMarkup().add(
						types.InlineKeyboardButton("Скачать ⬇️", url=last_loop[0])
					)

					for user in sqlite.get_users_with_sub():
						try:
							await bot.send_audio(user, last_loop[0], caption=caption, reply_markup=markup)
							sqlite.increment_user_samples(user)
						except Exception as ex:
							logger.warning(ex)

					loops_count1 = loops_count2

				await asyncio.sleep(0.125)
		except Exception as ex:
			logger.critical(ex)
			await asyncio.sleep(3)
