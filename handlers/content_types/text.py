from aiogram import types
import time
import logging
#############################
from main import dp, bot
from data import BOT_AUTHOR, RATE_LIMIT
from unix import unix_to_date
from utils import rate_limit
from keyboards import subscribe_markup
import sqlite

logger = logging.getLogger("bot.handlers.content_types.text")

@rate_limit(limit=RATE_LIMIT)
@dp.message_handler(lambda message: "профиль" in message.text.lower())
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

@rate_limit(limit=RATE_LIMIT)
@dp.message_handler(lambda message: "обратная связь" in message.text.lower())
async def feedback(message: types.Message) -> None:
	try:
		await message.answer(f"Столкнулись с какой-либо проблемой в процессе использования бота \
или хотите предложить интересное нововведение? Обращайтесь. <b>{BOT_AUTHOR}</b>\n\n\
Форма обращения:\n\
<b>1.</b> {message.from_user.id} (это ваш идентификатор)\n\
<b>2.</b> Суть обращения\n\
<b>3.</b> Дата и время, когда вы столкнулись с проблемой.\n\
<b>4.</b> Скриншоты/сообщения от бота в качестве доказательства.")
	except Exception as ex:
		logger.warning(ex)

@rate_limit(limit=RATE_LIMIT)
@dp.message_handler(lambda message: "подписка" in message.text.lower())
async def feedback(message: types.Message) -> None:
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

@rate_limit(limit=RATE_LIMIT)
@dp.message_handler(lambda message: "помощь" in message.text.lower())
async def feedback(message: types.Message) -> None:
	try:
		await bot.send_photo(message.chat.id, 
				"https://i.postimg.cc/rpzVt1v0/help.jpg", 
				caption=f"<b>Как пользоваться ботом?</b>\n\n\
Всё довольно просто, вы будете получать все новые сэмплы автоматически. \
Как только на сайте <i>looperman.com</i> выходит один семпл - он сразу же отправляется Вам!\n\
Скачать вы его сможете <b>прямо в телеграме</b>, либо нажав на кнопку \"<b>Скачать</b> ⬇️\".\n\n\
Остались вопросы? Пиши. <b>{BOT_AUTHOR}</b>"
			)
	except Exception as ex:
		logger.warning(ex)

@rate_limit(limit=RATE_LIMIT)
@dp.message_handler(content_types=types.ContentType.TEXT)
async def feedback(message: types.Message) -> None:
	try:
		await message.reply("<b>Я тебя не понимаю.</b>\nИспользуй команды или кнопки навигации.")
	except Exception as ex:
		logger.warning(ex)