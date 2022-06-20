from aiogram import Dispatcher
from .throttling import ThrottlingMiddleware

def setup(dp: Dispatcher) -> None:
	dp.middleware.setup(ThrottlingMiddleware())