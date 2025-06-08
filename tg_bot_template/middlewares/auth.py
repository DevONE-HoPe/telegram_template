from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger

from tg_bot_template.core.config import settings
from tg_bot_template.services.users import add_user, user_exists

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import TelegramObject
    from sqlalchemy.ext.asyncio import AsyncSession


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        session: AsyncSession = data["session"]
        message: Message = event
        user = message.from_user

        if not user:
            return await handler(event, data)

        if await user_exists(session, user.id):
            return await handler(event, data)

        # 1 проверка на наличие username
        if not user.username:
            await asyncio.sleep(2)
            register_failed: str = (
                "Для регистрации заполните, пожалуйста, Имя пользователя в своем профиле, иначе вас не "
                "смогут найти другие участники!"
            )
            await message.answer(register_failed)
            return

        # 2 проверка на наличие passphrase
        passphrase = settings.REGISTER_PASSPHRASE
        if passphrase is not None and message.text != passphrase:
            await asyncio.sleep(2)
            await message.answer("Enter passphrase for register in bot:")
            return

        logger.info(
            f"new user registration | user_id: {user.id} | message: {message.text}"
        )

        await add_user(session=session, user_id=user.id, username=user.username)

        return await handler(event, data)
