from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import COINS, TIMEFRAMES


def get_coin_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text=COINS[0])
    builder.button(text=COINS[1])
    builder.button(text=COINS[2])
    builder.button(text=COINS[3])
    builder.button(text=COINS[4])
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
