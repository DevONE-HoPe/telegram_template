from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="Нажми меня")],
        [KeyboardButton(text="Рейтинг")],
        [KeyboardButton(text="Мой профиль")],
    ]

    keyboard = ReplyKeyboardBuilder(markup=buttons)

    keyboard.adjust(1)

    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)
