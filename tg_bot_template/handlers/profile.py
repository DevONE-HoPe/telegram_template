from __future__ import annotations
from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from tg_bot_template.keyboards.reply.cancel import cancel_keyboard
from tg_bot_template.keyboards.reply.menu import main_keyboard
from tg_bot_template.states.states import UserForm
from tg_bot_template.services.users import update_user_profile

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = Router()

@router.message(F.text == "Мой профиль")
async def handle_profile_button(message: Message, state: FSMContext):
    text = "Напишите ваше имя"
    
    keyboard = cancel_keyboard()
    
    await state.set_state(UserForm.name)
    
    await message.answer(
        text=text,
        reply_markup=keyboard
    )

@router.message(UserForm.name, F.text.strip() != "", lambda message: len(message.text.strip()) <= 30)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(UserForm.info)
    await message.answer(
        "Отлично, записал. Теперь немного расскажите о себе.",
        reply_markup=cancel_keyboard()
    )

@router.message(UserForm.name)
async def process_invalid_name(message: Message):
    await message.reply("Я тебя не понял, попробуй по новой :(")

@router.message(UserForm.info, F.text, F.text.strip() != "", lambda message: len(message.text.strip()) <= 100)
async def process_info(message: Message, state: FSMContext):
    await state.update_data(info=message.text.strip())
    await state.set_state(UserForm.photo)
    await message.answer(
        "Отлично, записал. Теперь скиньте свое фото.",
        reply_markup=cancel_keyboard()
    )

@router.message(UserForm.info)
async def process_invalid_info(message: Message):
    await message.reply("Я тебя не понял, попробуй по новой :(\nИнформация должна быть текстом и не более 100 символов.")

@router.message(UserForm.photo, F.photo)
async def process_photo(message: Message, state: FSMContext, session: AsyncSession):
    photo_file_id = message.photo[-1].file_id

    await state.update_data(photo=photo_file_id)

    data = await state.get_data()

    await update_user_profile(
        session=session,
        user_id=message.from_user.id,
        name=data.get('name'),
        info=data.get('info'),
        photo=data.get('photo')
    )

    await state.clear()

    await message.answer(
        "Готово, данные обновлены.",
        reply_markup=main_keyboard()
    )
    

@router.message(UserForm.photo)
async def process_invalid_photo(message: Message):
    await message.reply("Я тебя не понял, попробуй по новой :(\nНужно отправить фото.")