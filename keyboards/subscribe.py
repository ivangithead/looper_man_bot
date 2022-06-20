from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import *

subscribe_markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(
	InlineKeyboardButton(text=f"Продлить подписку на 3 дня [{SUBSCRIBE_3_DAYS} RUB] 💵", callback_data="buy3days"),
	InlineKeyboardButton(text=f"Продлить подписку на 7 дней [{SUBSCRIBE_7_DAYS} RUB] 💵", callback_data="buy7days"),
	InlineKeyboardButton(text=f"Продлить подписку на 30 дней [{SUBSCRIBE_30_DAYS} RUB] 💵", callback_data="buy30days"),
	InlineKeyboardButton(text=f"Купить подписку навсегда [{SUBSCRIBE_FOREVER} RUB] ⚡️", callback_data="buyforever")
)