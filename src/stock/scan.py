import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from data import MarketDB

from mplfinance.original_flavor import candlestick_ohlc
from MACD import MACD
from OHLC import OHLC
import numpy as np

mk = MarketDB.MarketDB()

codes = mk.get_codes().values()
for code in codes:
    df = mk.get_daily_price(code, '2018-08-01')
    macd = MACD(df)
    trading_points = macd.get_trading_points()
    if len(trading_points) == 0:
        continue

    if trading_points[-1].get("x") >= mdates.date2num(np.datetime64("2021-02-18")) and \
            trading_points[-1].get("trading") == "buy":
        print(code)