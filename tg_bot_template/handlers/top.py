from __future__ import annotations
from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.types import Message
from tg_bot_template.services.users import (
    get_user_taps,
    get_top_users_by_taps,
    get_total_taps,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.message(F.text == "Рейтинг")
async def handle_rating_button(message: Message, session: AsyncSession):
    user_id = message.from_user.id

    user_taps = await get_user_taps(session, user_id)

    total_taps = await get_total_taps(session)

    top_users = await get_top_users_by_taps(session, limit=1)

    if not top_users:
        await message.answer("Пока нет данных о рейтинге")
        return

    top_user = top_users[0]

    name = top_user.name or ""
    username = f"[@{top_user.username}]" if top_user.username else ""
    info = top_user.info or ""

    caption = f"""Лучший жмакер:
    {name}{username}
    {info}

    Всего нажатий твоих: {user_taps}
    Всего нажатий: {total_taps}"""

    if top_user.photo:
        await message.answer_photo(photo=top_user.photo, caption=caption)
    else:
        await message.answer(caption)
