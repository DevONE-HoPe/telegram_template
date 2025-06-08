from aiogram import Router, types
from aiogram.filters import Command

from tg_bot_template.filters.admin import AdminFilter

router = Router()

@router.message(Command("creator"), AdminFilter())
async def help_handler(message: types.Message) -> None:
    await message.answer("Master?")