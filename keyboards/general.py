from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

general_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
	KeyboardButton("👤 Профиль"),
	KeyboardButton("✉️ Обратная связь"),
	KeyboardButton("🎶 Подписка"),
	KeyboardButton("🆘 Помощь")
)