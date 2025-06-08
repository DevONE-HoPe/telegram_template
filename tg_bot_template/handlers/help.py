from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def help_handler(message: types.Message) -> None:
    help_text = """
Бот для соревнования по тыканью по кнопке. Тыкай в кнопку и побеждай!
    """
    await message.answer(help_text)
