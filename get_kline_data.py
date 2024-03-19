from pybit.unified_trading import HTTP
import datetime as dt
import matplotlib.pyplot as plt



def get_kline_data(ticker: str, interval: int, start_time: dt.datetime):
    timestamp_start = int(start_time.timestamp() * 1000)
    timestamp_end = int(dt.datetime.now().timestamp() * 1000)
    response = session.get_kline(category='linear',
                                 symbol=ticker,
                                 interval=interval,
                                 start=timestamp_start,
                                 end=timestamp_end).get('result').get('list')
    timestamps = [int(entry[0]) for entry in response]
    prices = [float(entry[1]) for entry in response]
    dates = [dt.datetime.utcfromtimestamp(ts / 1000) for ts in timestamps]
    sorted_data = sorted(zip(dates, prices))
    sorted_dates = [date.strftime('%H:%M') for date, _ in sorted_data]
    sorted_prices = [price for _, price in sorted_data]
    # return sorted_dates, sorted_prices

    return {"dates": sorted_dates, "prices": sorted_prices}


def get_kline_data_day(ticker: str, interval: int):
    start_time = dt.datetime.now() - dt.timedelta(days=1)
    return get_kline_data(ticker, interval, start_time)


# def get_kline_data_3hour(ticker: str, interval: int):
#     start_time = dt.datetime.now() - dt.timedelta(hours=3)
#     return get_kline_data(ticker, interval, start_time)


# def get_kline_data_1hour(ticker: str, interval: int):
#     start_time = dt.datetime.now() - dt.timedelta(hours=1)
#     return get_kline_data(ticker, interval, start_time)

def get_kline_data_hour(ticker: str, interval: int):
    start_time = dt.datetime.now() - dt.timedelta(hours=interval)
    return get_kline_data(ticker, interval, start_time)


key = 'u8O8XqBFrvccyI71Aj'
secret = 'TY2ekPsMXY5ALy2zmWEctTdI7ERodHn8x2JB'
session = HTTP(
    testnet=False,
    api_key=key,
    api_secret=secret)

# tickers = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']  # варианты того, что мы будем искать
# dates, prices = get_kline_data_hour("BTCUSDT", 1)  # тут ебашишь и вызываешь необходимую из 3-х функций( название),
# # Interval - временной шаг на графике потом


def create_plot(dates, prices, title = ""):
    plt.figure(figsize=(10, 5))
    for i in range(1, len(prices)):
        color = 'green' if prices[i] > prices[i - 1] else 'red'
        plt.plot([dates[i - 1], dates[i]], [prices[i - 1], prices[i]], marker='o', color=color)
    plt.xlabel('Time')
    plt.ylabel('Price')

    plt.xticks(dates[::5] + [dates[-1]])

    plt.grid(True)

    plt.title(title)
    plt.savefig('price_vs_time_plot.png')  # сохранение графика для отправки пользовтаелю

# create_plot(dates, prices)