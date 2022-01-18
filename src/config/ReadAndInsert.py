import calendar
import json
import pandas as pd
import pymysql
import requests
import sys
from Query import Query
from bs4 import BeautifulSoup
from datetime import datetime
import threading


class ReadAndInsert:
    __conn = None
    __query = None
    __idx = None
    __id = None
    __name = None
    __pages_to_fetch = None

    def __init__(self, query, idx, id, name, pages_to_fetch):
        self.__conn = self.__get_init_db()
        self.__query = query
        self.__idx = idx
        self.__id = id
        self.__name = name
        self.__pages_to_fetch = pages_to_fetch

        df = self.get_daily_data(self.__id, self.__name, self.__pages_to_fetch)
        if df is None:
            return
        self.update_daily_price_and_volume(df, self.__idx, self.__id, self.__name)

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.__conn.close()

    def __get_init_db(self):
        try:
            with open('config-db.json', 'r') as in_file:
                config = json.load(in_file)
                host = config['host']
                user = config['user']
                password = config['password']
                db = config['db']
        except FileNotFoundError:
            print('생성된 "config-db.json" 파일에 DB 정보를 기입 후, 다시 실행하세요.')
            with open('config-db.json', 'w') as out_file:
                config = {'host': 'localhost', 'user': 'user', 'password': 'password', 'db': 'db'}
                json.dump(config, out_file)
            sys.exit()

        return pymysql.connect(host=host, user=user, password=password, db=db)


    def get_daily_data(self, id, name, pages_to_fetch):
        """네이버에서 주식 시세를 읽어서 데이터프레임으로 반환"""
        try:
            url = f"http://finance.naver.com/item/sise_day.nhn?code={id}"
            html = BeautifulSoup(requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text, "lxml")
            has_data = html.find("td", class_="pgRR") is not None
            if not has_data:
                return None

            df = pd.DataFrame()
            last_page_num = str(html.find("td", class_="pgRR").a["href"]).split('=')[-1]
            pages = min(int(last_page_num), pages_to_fetch)
            for page in range(1, pages + 1):
                at_page_url = f'{url}&page={page}'
                df = df.append(pd.read_html(requests.get(at_page_url, headers={'User-agent': 'Mozilla/5.0'}).text)[0])
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                # print(f'[{tmnow}] {name} ({id}) : {page:04d}/{pages:04d} pages are downloading...', end="\r")
            df = df.rename(columns={
                '날짜': 'date',
                '종가': 'close',
                '전일비': 'diff',
                '시가': 'open',
                '고가': 'high',
                '저가': 'low',
                '거래량': 'volume'
            })
            df['date'] = df['date'].replace('.', '-')
            df = df.dropna()
            df[[
                'close',
                'diff',
                'open',
                'high',
                'low',
                'volume'
            ]] = df[[
                'close',
                'diff',
                'open',
                'high',
                'low',
                'volume'
            ]].astype(int)
            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]
        except Exception as e:
            print('Exception occured :', str(e))
            return None
        return df


    def update_daily_price_and_volume(self, df, num, id, name):
        """네이버에서 읽어온 주식 시세를 DB에 REPLACE"""
        with self.__conn.cursor() as curs:
            for r in df.itertuples():
                # 일별 가격 추가
                curs.execute(self.__query.replace_into_daily_price(id, r.date, r.open, r.high, r.low, r.close))
                # 일별 거래량 추가
                curs.execute(self.__query.replace_into_daily_volume(id, r.date, r.volume))
            self.__conn.commit()
            print(f'[SUCCESS] #{num + 1:04d} {name} ({id}) : {len(df)} REPLACE INTO daily_price')