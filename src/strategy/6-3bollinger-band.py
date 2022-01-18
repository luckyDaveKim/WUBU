import matplotlib.pyplot as plt
from investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('안랩', '2019-01-02')

c = 1.5
df['MA20'] = df['close'].rolling(window=20).mean()  # ①
df['stddev'] = df['close'].rolling(window=20).std()  # ②
df['upper'] = df['MA20'] + (df['stddev'] * 2)  # ③
df['uppersub'] = df['MA20'] + (df['stddev'] * c)  # ③
df['lower'] = df['MA20'] - (df['stddev'] * 2)  # ④
df['lowersub'] = df['MA20'] - (df['stddev'] * c)  # ④
df = df[19:]  # ⑤

over_count = 0
over_sub_count = 0
for index, row in df.iterrows():
    if (row['close'] > row['upper'] or row['close'] < row['lower']):
        over_count += 1
    elif (row['close'] > row['uppersub'] or row['close'] < row['lowersub']):
        over_sub_count += 1

print(f'total : {df.size},over count : {over_count}, over sub count : {over_count + over_sub_count}')
print(f'over per : {over_count / df.size}, over sub per : {(over_count + over_sub_count) / df.size}')


plt.figure(figsize=(9, 5))
plt.plot(df.index, df['close'], color='#0000ff', label='Close')  # ⑥
plt.plot(df.index, df['upper'], 'r--', label='Upper band')  # ⑦
plt.plot(df.index, df['uppersub'], '--', color='#550000', label='Upper Sub band')  # ⑦
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.plot(df.index, df['lowersub'], '--', color='#005500', label='Lower Sub band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')  # ⑧
plt.legend(loc='best')
plt.title('NAVER Bollinger Band (20 day, 2 std)')
plt.show()