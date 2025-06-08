from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

def register_middlewares(dp: Dispatcher) -> None:
    from .auth import AuthMiddleware
    from .database import DatabaseMiddleware

    dp.update.outer_middleware(DatabaseMiddleware())

    dp.message.middleware(AuthMiddleware())

    dp.callback_query.middleware(CallbackAnswerMiddleware())