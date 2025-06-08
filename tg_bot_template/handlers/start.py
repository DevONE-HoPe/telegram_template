from aiogram import Router, types
from aiogram.filters import CommandStart

from tg_bot_template.keyboards.reply.menu import main_keyboard

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    await message.answer("Добро пожаловать в главное меню", reply_markup=main_keyboard())