from aiogram import types
import logging
#######################################
from main import dp, bot
from data import BOT_AUTHOR, RATE_LIMIT
from utils import rate_limit

logger = logging.getLogger("bot.handlers.commands.help")

@rate_limit(limit=RATE_LIMIT)
@dp.message_handler(commands=["help", "помощь"])
async def help(message: types.Message) -> None:
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