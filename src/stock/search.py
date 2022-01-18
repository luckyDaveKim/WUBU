import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from data import MarketDB

from mplfinance.original_flavor import candlestick_ohlc
from MACD import MACD
from OHLC import OHLC

mk = MarketDB.MarketDB()

df = mk.get_daily_price('명신산업', '2018-08-01')

ohlc = OHLC(df)
macd = MACD(df)

val = []
for point in macd.get_trading_points():
    pass

val2 = []
for point in macd.get_trading_points2():
    pass

plt.figure(figsize=(9, 7))

p1 = plt.subplot(2, 1, 1)
plt.title('Triple Screen Trading - First Screen (NCSOFT)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.get_ohlc_data(), width=.1, colorup='red', colordown='blue')  # ⑦
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
for trading_point in macd.get_trading_points():
    plt.plot(trading_point.get("x"), trading_point.get("y"), trading_point.get("marker"))

p2 = plt.subplot(2, 1, 2)
plt.grid(True)
p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
macd_histogram_data = macd.get_histogram_data()
plt.bar(macd_histogram_data.get("x"), macd_histogram_data.get("y"), color='m', label='MACD-Hist')
macd_data = macd.get_macd_data()
plt.plot(macd_data.get("x"), macd_data.get("y"), color='b', label='MACD')
macd_signal_data = macd.get_signal_data()
plt.plot(macd_signal_data.get("x"), macd_signal_data.get("y"), 'g--', label='MACD-Signal')
plt.legend(loc='best')

plt.show()
