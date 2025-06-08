from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class GameButtonCallback(CallbackData, prefix="game"):
    action: str  # tap
    tap_count: int  # сколько тапов уже было


def create_game_keyboard(current_taps: int = 0):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Нажми меня",
        callback_data=GameButtonCallback(action="tap", tap_count=current_taps),
    )

    return builder.as_markup()
