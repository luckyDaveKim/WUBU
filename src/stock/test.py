from itertools import islice

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from data import MarketDB
import numpy as np

from Wallet import Wallet

mk = MarketDB.MarketDB()
wallet = Wallet(10_000_000)

def is_low_price(stock, startDate, endDate):
    df = mk.get_daily_price(stock, startDate, endDate)

    df['MA20'] = df['close'].rolling(window=20).mean()
    df['stddev'] = df['close'].rolling(window=20).std()
    df['upper'] = df['MA20'] + (df['stddev'] * 2)
    df['lower'] = df['MA20'] - (df['stddev'] * 2)
    df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])
    df['PBMA5'] = df['PB'].rolling(window=5).mean()
    df['gradient'] = df['PB'] - df['PBMA5']
    df['II'] = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    df['IIP21'] = df['II'].rolling(window=21).sum() / df['volume'].rolling(window=21).sum() * 100
    df = df.dropna()
    df['number'] = range(len(df['close']))
    print(df)

    manage_stock_count = 1000

    plt.figure(figsize=(9, 9))
    p1 = plt.subplot(3, 1, 1)
    p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.title('SK Hynix Bollinger Band(20 day, 2 std) - Reversals')
    plt.plot(df.index, df['close'], 'm', label='Close')
    plt.plot(df.index, df['upper'], 'r--', label='Upper band')
    plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
    plt.plot(df.index, df['lower'], 'c--', label='Lower band')
    plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')

    for i, data in islice(df.iterrows(), 1, None):
        beforeIndex = data['number']-1
        is_pb_10 = df['PB'].iloc[beforeIndex] <= 1 and data['PB'] >= 1
        is_pb_07 = df['PB'].iloc[beforeIndex] <= 0.7 and data['PB'] >= 0.7
        is_pb_05 = df['PB'].iloc[beforeIndex] >= 0.5 and data['PB'] <= 0.5
        is_pb_0 = df['PB'].iloc[beforeIndex] >= 0 and data['PB'] <= 0
        if is_pb_10:
            sell_stock = wallet.get_stock()
            if sell_stock > 0:
                print(data.date)
                wallet.sell(data['close'], sell_stock)
                plt.plot(data.date, data.close, 'bv')
        elif is_pb_07:
            sell_stock = wallet.get_stock() - (manage_stock_count * 0.5)
            if sell_stock > 0:
                print(data.date)
                wallet.sell(data['close'], sell_stock)
                plt.plot(data.date, data.close, 'bv')
        elif is_pb_05:
            buy_stock = (manage_stock_count * 0.5) - wallet.get_stock()
            if buy_stock > 0:
                print(data.date)
                wallet.buy(data['close'], buy_stock)
                plt.plot(data.date, data.close, 'r^')
        elif is_pb_0:
            buy_stock = manage_stock_count - wallet.get_stock()
            if buy_stock > 0:
                print(data.date)
                wallet.buy(data['close'], buy_stock)
                plt.plot(data.date, data.close, 'r^')

    print(f"money:{wallet.get_money() + (wallet.get_stock() * df['close'].iloc[-1])}")

    plt.legend(loc='best')

    p2 = plt.subplot(3, 1, 2)
    p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.plot(df.index, df['PB'], 'b', label='%b')
    plt.grid(True)
    plt.legend(loc='best')

    p3 = plt.subplot(3, 1, 3)
    p3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.bar(df.index, df['IIP21'], color='g', label='II% 21day')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()

    # try:
    #     if df['PB'].values[-1] < 0.25:
    #         # print(f"stock: {stock}, mid: {df['MA20'].iloc[-1]}, price: {df['close'].iloc[-1]}")
    #         return True
    # except BaseException as e:
    #     print(f'Exception!!! {stock}; {e}')
    #     return False
    #
    # return False

# codes = mk.get_codes().values()
# low_codes = []
# for code in codes:
#     # print(code)
#     if is_low_price(code):
#         low_codes.append(code)
#
# print(low_codes)

is_low_price('안랩', '2018-01-01', '2021-03-01')