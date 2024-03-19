import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import TOKEN, COINS, TIMEFRAMES
from keyboards import get_coin_keyboard, get_timeframe_keyboard
from get_trader_info import get_data
from get_kline_data import get_kline_data_day, get_kline_data_hour, create_plot


client_router = Router()

class ClientState(StatesGroup):
    '''Хранит на каком этапе диалога находится клиент'''
    START_COIN = State()
    COIN_SELECTED = State()
    TIMEFRAME_SELECTED = State()


@client_router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await state.set_state(ClientState.START_COIN)
    await message.answer('*приветствие*', 
                         reply_markup=get_coin_keyboard())


@client_router.message(ClientState.START_COIN)
async def choose_coin_process(message: Message, state: FSMContext):
    if message.text in COINS:
        await state.update_data(COIN=message.text)
        
        await message.answer('Выберите период...', 
                            reply_markup=get_timeframe_keyboard())
        await state.set_state(ClientState.COIN_SELECTED) 
    else:
        await message.answer('Выберите монету, нажав на одну из кнопок') 


@client_router.message(ClientState.COIN_SELECTED)
async def choose_timeframe_process(message: Message, state: FSMContext):
    if message.text in TIMEFRAMES:
        await state.update_data(TIMEFRAME=message.text)

        user_state_data = await state.get_data()
        coin = user_state_data['COIN']
        timeframe = user_state_data['TIMEFRAME']


        kline_data = None
        if timeframe == '1 день':
            kline_data = get_kline_data_day(COINS[coin], 1)
        elif timeframe == '3 часа':
            kline_data = get_kline_data_hour(COINS[coin], 3)
        elif timeframe == '1 час':
            kline_data = get_kline_data_hour(COINS[coin], 1)

        if kline_data:
            create_plot(kline_data["dates"], kline_data["prices"], COINS[coin])

            cat = FSInputFile("price_vs_time_plot.png")
            await message.answer_photo(cat, caption=f'{COINS[coin]} | {timeframe}', reply_markup=get_coin_keyboard())

        await state.set_state(ClientState.START_COIN)
        # await state.clear()
    elif message.text == '🚪Назад':
        await state.set_state(ClientState.START_COIN)
        await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь', 
                         reply_markup=get_coin_keyboard())
    else:
        await message.answer('Выберите период, нажав на одну из кнопок') 



@client_router.message(Command("help"))
async def process_help_command(message: Message):
    await message.answer(
        'info'
    )



async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(client_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
