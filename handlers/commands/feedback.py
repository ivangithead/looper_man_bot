from aiogram import types
import logging
#######################################
from main import dp
from data import BOT_AUTHOR, RATE_LIMIT
from utils import rate_limit
import sqlite

logger = logging.getLogger("bot.handlers.commands.feedback")

@rate_limit(limit=RATE_LIMIT)
@dp.message_handler(commands=["feedback"])
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