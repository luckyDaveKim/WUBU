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
import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from db_manager import DBManager

db_manger = DBManager()

date = '2021-09-17'

url = "https://m.search.naver.com/p/csearch/content/qapirender.nhn?_callback=a&pkid=141&key=exchangeApiBasic&where=nexearch&q=%ED%99%98%EC%9C%A8&u6=standardUnit&u7=0&u3=USD&u4=KRW&u2=1&u1=keb&u8=down&u5=all&_=1631993425743"

text = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text[2:-2]
jsonText = json.loads(text)
# print(jsonText['itemList']['chardData'][0]['data']['List'][0])
# print(jsonText['itemList']['chardData'][0]['data']['List'][1])
data = jsonText['itemList']['chardData'][0]['data']['List']
timeList = data[0]
rateList = data[1]

items = []
for i, val in enumerate(timeList):
    time = timeList[i]
    rate = rateList[i]

    item = {
        'datetime': f'{date} {str(time).zfill(6)}',
        'rate': rate
    }
    items.append(item)

db_manger.insert_minutely_exchange_rate(items)