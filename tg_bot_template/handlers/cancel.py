from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot_template.keyboards.reply.menu import main_keyboard

router = Router()

@router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Принял, отбой, возвращаюсь в главное меню.", reply_markup=main_keyboard())