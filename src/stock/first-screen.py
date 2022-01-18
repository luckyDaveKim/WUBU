import matplotlib.pyplot as plt
import numpy
import pandas
from mplfinance.original_flavor import candlestick_ohlc

from data import MarketDB2
import matplotlib.dates as mdates

# 매수, 매도, 관망중 하나의 선택지를 제거할 수 있다.

mk = MarketDB2.MarketDB()
df = mk.get_minly_price('삼성전자', '2020-01-03 10:05:00', '2020-01-03 11:10:00')

ema60 = df.cur_price.ewm(span=60).mean()  # ① 종가의 12주 지수 이동평균
ema130 = df.cur_price.ewm(span=130).mean()  # ② 종가의 12주 지수 이동평균
macd = ema60 - ema130  # ③ MACD선
signal = macd.ewm(span=45).mean()  # ④ 신호선(MACD의 9주 지수 이동평균)
macdhist = macd - signal  # ⑤ MACD 히스토그램

df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal,
               macdhist=macdhist).dropna()

# df['number'] = df.datetime.dt.strftime('%H:%M')
df['number'] = df.datetime.dt.strptime('%Y-%m')
# df['number'] = pandas.to_datetime(df.index)  # ⑥
ohlc = df[['datetime', 'start_price', 'high_price', 'low_price', 'cur_price']]
print(df)

x = numpy.arange(len(df.index))

plt.figure(figsize=(9, 7))
p1 = plt.subplot(2, 1, 1)
plt.title('Triple Screen Trading - First Screen (NCSOFT)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')  # ⑦
# p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# plt.plot(x, df['ema130'], color='c', label='EMA130')
plt.legend(loc='best')

# p2 = plt.subplot(2, 1, 2)
# plt.grid(True)
# # p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# plt.bar(df.number, df['macdhist'], color='m', label='MACD-Hist')
# plt.plot(df.number, df['macd'], color='b', label='MACD')
# plt.plot(df.number, df['signal'], 'g--', label='MACD-Signal')
# plt.legend(loc='best')
# plt.show()
