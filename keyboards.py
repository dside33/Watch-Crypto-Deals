from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

from config import COINS, TIMEFRAMES


def get_coin_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for coin_name, _ in COINS.items():
        builder.add(KeyboardButton(text=coin_name)) 

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True,
                             input_field_placeholder = 'Выберите монету...')


def get_timeframe_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text=TIMEFRAMES[0])
    builder.button(text=TIMEFRAMES[1])
    builder.button(text=TIMEFRAMES[2])
    builder.button(text='🚪Назад')
    builder.adjust(3)

    return builder.as_markup(resize_keyboard=True,
                             input_field_placeholder = 'Выберите период...')
