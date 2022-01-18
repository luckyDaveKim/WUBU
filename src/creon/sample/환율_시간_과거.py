import json
import re
from datetime import datetime, timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup

from db_manager import DBManager

db_manger = DBManager()

date = datetime.now()
# date = datetime(2021, 9, 23)
deltaTime = timedelta(days=-1)

for i in range(1, 2):
    print('find at {}'.format(date.strftime('%Y%m%d')))
    url = "https://www.kebhana.com/cms/rate/wpfxd651_07i_01.do"
    payload = {
        "curCd": "USD",
        "inqDt": date.strftime('%Y%m%d')
    }
    html = requests.post(url, headers={'User-agent': 'Mozilla/5.0'}, data=payload).text

    df = pd.DataFrame()
    df = df.append(pd.read_html(html))
    df = df.rename(columns={
        '시간': 'time',
        '매매기준율': 'rate'
    })
    df = df[['time', 'rate']]

    # print(df)
    db_manger.insert_minutely_exchange_rate(date.strftime('%Y-%m-%d'), df)

    date = date + deltaTime
