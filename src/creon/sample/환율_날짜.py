# 하나은행
# - 시간 나오는 데이터
# https://m.search.naver.com/p/csearch/content/qapirender.nhn?_callback=a&pkid=141&key=exchangeApiBasic&where=nexearch&q=%ED%99%98%EC%9C%A8&u6=standardUnit&u7=0&u3=USD&u4=KRW&u2=1&u1=keb&u8=down&u5=all&_=1631993425743
# - 고시 회차 나오는 데이터
# https://finance.naver.com/marketindex/exchangeDegreeCountQuote.naver?marketindexCd=FX_USDKRW&page=1
# - 일별 데이터
# https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW&page=2
#
# 신한은행
# - 시간 나오는 데이터
# https://finance.naver.com/marketindex/exchangeDegreeCountQuote.naver?marketindexCd=FX_USDKRW_SHB&page=2
# - 고시 회차 나오는 데이터
# https://m.search.naver.com/p/csearch/content/qapirender.nhn?_callback=a&pkid=141&key=exchangeApiBasic&where=nexearch&q=%ED%99%98%EC%9C%A8&u6=standardUnit&u7=0&u3=USD&u4=KRW&u2=1&u1=shb&u8=down&u5=all&_=1631993425742
# - 일별 데이터
# https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW_SHB&page=2
#
#
# 한국수출입은행
# https://www.koreaexim.go.kr/site/program/openapi/openApiView?menuid=001003002002001&apino=2&viewtype=C
#
# 두나무
# https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from db_manager import DBManager

db_manger = DBManager()

url = "https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW"

for page in range(1, 4):
    page_url = '{}&page={}'.format(url, page)

    df = pd.DataFrame()
    df = df.append(pd.read_html(requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text)[0])
    df = df.rename(columns={
        '날짜': 'date',
        '매매기준율': 'rate'
    })
    df[['rate']] = df[['rate']].astype(float)
    df = df[['date', 'rate']]

    db_manger.insert_daily_exchange_rate(df)
