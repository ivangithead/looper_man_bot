from aiogram import types
import logging
#########################
from main import dp, bot
from data import *
import p2p
import sqlite

logger = logging.getLogger("bot.callback.bill")

@dp.callback_query_handler(lambda call: call.data == "buy3days")
async def callback(call: types.CallbackQuery) -> None:
	try:
		bill    = p2p.create_bill(SUBSCRIBE_3_DAYS)
		url     = bill[1]
		bill_id = bill[0]

		markup = types.InlineKeyboardMarkup().row(
			types.InlineKeyboardButton(text="Оплатить", url=url),
			types.InlineKeyboardButton(text="Я оплатил", callback_data=f"ipaid|{bill_id}|3"),
		)

		await bot.send_message(
			call.from_user.id, 
			f"<b>• ДОСТУП НА 3 ДНЯ •</b>\n\n\
Оплатите <b><a href=\"{bill[1]}\">этот счёт</a></b> в течении часа.\n\
После оплаты <b>ОБЯЗАТЕЛЬНО</b> нажмите кнопку <b>\"Я оплатил ✌🏻\"</b>.",
	   		reply_markup=markup
			)
	except Exception as ex:
		logger.error(ex)

@dp.callback_query_handler(lambda call: call.data == "buy7days")
async def callback(call: types.CallbackQuery) -> None:
	try:
		bill    = p2p.create_bill(SUBSCRIBE_7_DAYS)
		url     = bill[1]
		bill_id = bill[0]

		markup = types.InlineKeyboardMarkup().row(
			types.InlineKeyboardButton(text="Оплатить", url=url),
			types.InlineKeyboardButton(text="Я оплатил", callback_data=f"ipaid|{bill_id}|7"),
		)

		await bot.send_message(
			call.from_user.id, 
			f"<b>• ДОСТУП НА 7 ДНЕЙ •</b>\n\n\
Оплатите <b><a href=\"{bill[1]}\">этот счёт</a></b> в течении часа.\n\
После оплаты <b>ОБЯЗАТЕЛЬНО</b> нажмите кнопку <b>\"Я оплатил ✌🏻\"</b>.",
	   		reply_markup=markup
			)
	except Exception as ex:
		logger.error(ex)

@dp.callback_query_handler(lambda call: call.data == "buy30days")
async def callback(call: types.CallbackQuery) -> None:
	try:
		bill    = p2p.create_bill(SUBSCRIBE_30_DAYS)
		url     = bill[1]
		bill_id = bill[0]

		markup = types.InlineKeyboardMarkup().row(
			types.InlineKeyboardButton(text="Оплатить", url=url),
			types.InlineKeyboardButton(text="Я оплатил", callback_data=f"ipaid|{bill_id}|30"),
		)

		await bot.send_message(
			call.from_user.id, 
			f"<b>• ДОСТУП НА 30 ДНЕЙ •</b>\n\n\
Оплатите <b><a href=\"{bill[1]}\">этот счёт</a></b> в течении часа.\n\
После оплаты <b>ОБЯЗАТЕЛЬНО</b> нажмите кнопку <b>\"Я оплатил ✌🏻\"</b>.",
	   		reply_markup=markup
			)
	except Exception as ex:
		logger.error(ex)

@dp.callback_query_handler(lambda call: call.data == "buyforever")
async def callback(call: types.CallbackQuery) -> None:
	try:
		bill    = p2p.create_bill(SUBSCRIBE_FOREVER)
		url     = bill[1]
		bill_id = bill[0]

		markup = types.InlineKeyboardMarkup().row(
			types.InlineKeyboardButton(text="Оплатить", url=url),
			types.InlineKeyboardButton(text="Я оплатил", callback_data=f"ipaid|{bill_id}|0"),
		)

		await bot.send_message(
			call.from_user.id, 
			f"<b>• ДОСТУП НАВСЕГДА •</b>\n\n\
Оплатите <b><a href=\"{bill[1]}\">этот счёт</a></b> в течении часа.\n\
После оплаты <b>ОБЯЗАТЕЛЬНО</b> нажмите кнопку <b>\"Я оплатил ✌🏻\"</b>.",
	   		reply_markup=markup
			)
	except Exception as ex:
		logger.error(ex)

@dp.callback_query_handler(lambda call: call.data.startswith("ipaid"))
async def callback(call: types.CallbackQuery) -> None:
	try:
		days      = int(call.data.split("|")[2])
		days_unix = days * 86400
		bill_id   = call.data.split("|")[1]
		status    = p2p.check_bill_state(bill_id)

		match status:
			case "PAID":
				await bot.delete_message(
					chat_id=call.from_user.id, 
					message_id=call.message.message_id
				)
				if days == 3:
					await bot.send_message(
						call.from_user.id, 
						"<b>Оплачено!</b> ✅\nВаша подписка продлена на 3 дня."
					)
				elif days == 7:
					await bot.send_message(
						call.from_user.id, 
						"<b>Оплачено!</b> ✅\nВаша подписка продлена на 7 дней."
					)
				elif days == 30:
					await bot.send_message(
						call.from_user.id, 
						"<b>Оплачено!</b> ✅\nВаша подписка продлена на 30 дней."
					)
				elif days == 0:
					await bot.send_message(
						call.from_user.id, 
						"<b>Оплачено!</b> ✅\nВы получили подписку навсегда."
					)

				if sqlite.get_user_subtime(call.from_user.id) != 0:
					sqlite.add_user_subtime(call.from_user.id, days_unix)
			case "WAITING":
				await bot.send_message(
					call.from_user.id,
					f"<b>Счёт ожидает оплаты.</b>\nЕсли вы оплатили счёт и ничего не произошло - сообщите <b>{BOT_AUTHOR}</b>"
				)
			case "REJECTED" | "EXPIRED":
				await bot.send_message(
					call.from_user.id,
					"<b>Счёт закрыт.</b>\nСоздайте новый и попробуйте снова."
				)
	except Exception as ex:
		logger.critical(ex)