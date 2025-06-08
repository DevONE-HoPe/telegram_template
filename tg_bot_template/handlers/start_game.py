from aiogram import Router, F
from aiogram.types import Message
from tg_bot_template.keyboards.inline.click import create_game_keyboard

router = Router()

@router.message(F.text == "Нажми меня")
async def handle_click_button(message: Message):
    last_session = 0
    
    text = f"Нажатий за последнюю сессию: {last_session}"
    
    keyboard = create_game_keyboard(current_taps=last_session)
    
    await message.answer(
        text=text,
        reply_markup=keyboard
    )