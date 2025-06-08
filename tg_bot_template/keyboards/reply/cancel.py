from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cancel_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="Отмена")],
    ]

    keyboard = ReplyKeyboardBuilder(markup=buttons)

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)