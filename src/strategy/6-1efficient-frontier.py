import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from investar import Analyzer

mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2016-01-04', '2018-04-27')['close']

print(f'###원천 데이터###\n{df}\n##########')


daily_ret = df.pct_change() #일간 수익률 (변동률)
print(f'###일간 수익률###\n{daily_ret}\n##########')

annual_ret = daily_ret.mean() * 246 #연간 수익률 = 일간 수익률 * 년평균 개장일
print(f'###연간 수익률###\n{annual_ret}\n##########')

daily_cov = daily_ret.cov() #일간 리스크 = 일간 수익률의 공분산
print(f'###일간 리스크###\n{daily_cov}\n##########')

annual_cov = daily_cov * 246 #연간 리스크 = 일간 리스크 * 년평균 개장일
print(f'###연간 리스크###\n{annual_cov}\n##########')

port_ret = []
port_risk = []
port_weights = []

for _ in range(3):
    weights = np.random.random(len(stocks)) #랜덤수 구함
    weights /= np.sum(weights) #랜덤수의 비중합이 1이 되도록 조정

    returns = np.dot(weights, annual_ret) #전체 수익률
    # 포트폴리오 리스크 = sqrt( (종목별 비중의 전치) * (종목별 연강 공분산 * 종목별 비중) )
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))
    print(f'weights: {weights}, risk: {risk}')

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)

portfolio = {'Returns': port_ret, 'Risk': port_risk}
for i, s in enumerate(stocks):
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk'] + [s for s in stocks]]

df.plot.scatter(x='Risk', y='Returns', figsize=(8, 6), grid=True)
plt.title('Efficient Frontier')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()