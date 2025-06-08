from __future__ import annotations
from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from tg_bot_template.services.users import increment_user_taps
from tg_bot_template.keyboards.inline.click import GameButtonCallback, create_game_keyboard

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.callback_query(GameButtonCallback.filter(F.action == "tap"))
async def handle_game_tap(query: CallbackQuery, callback_data: GameButtonCallback, session: AsyncSession) -> None:
    new_tap_count = callback_data.tap_count + 1
    await query.answer(f"Тап #{new_tap_count}!")
    
    new_keyboard = create_game_keyboard(new_tap_count)
    text = f"Нажатий за последнюю сессию: {new_tap_count}"

    await increment_user_taps(session=session, user_id=query.from_user.id)
    
    try:
        await query.message.edit_text(
            text=text,
            reply_markup=new_keyboard
        )
    except TelegramBadRequest:
        await query.message.answer(
            text=text,
            reply_markup=new_keyboard
        )