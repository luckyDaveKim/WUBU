import sys
from datetime import datetime
from threading import Timer

import calendar
import json
import pandas as pd
import pymysql
import requests
from bs4 import BeautifulSoup


class DBUpdater:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        try:
            with open('dbConfig.json', 'r') as in_file:
                config = json.load(in_file)
                host = config['host']
                user = config['user']
                password = config['password']
                db = config['db']
        except FileNotFoundError:
            print('생성된 "dbConfig.json" 파일에 DB 정보를 기입 후, 다시 실행하세요.')
            with open('dbConfig.json', 'w') as out_file:
                config = {'host': 'localhost', 'user': 'user',
                          'password': 'password', 'db': 'db'}
                json.dump(config, out_file)
            sys.exit()

        self.conn = pymysql.connect(host=host, user=user,
                                    password=password, db=db)

        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS company_info
            (
                id          varchar(20) not null primary key,
                name        varchar(40) null,
                last_update date        null
            )
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS daily_price
            (
                company_id varchar(20) not null,
                date       date        not null,
                open       bigint      null,
                high       bigint      null,
                low        bigint      null,
                close      bigint      null,
                primary key (company_id, date)
            )
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS daily_volume
            (
                company_id varchar(20) not null,
                date       date        not null,
                volume     bigint      null,
                primary key (company_id, date)
            )
            """
            curs.execute(sql)
        self.conn.commit()
        self.codes = dict()

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def read_krx_code(self):
        """KRX로부터 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=' \
              'download&searchType=13'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드': 'id', '회사명': 'name'})
        krx.id = krx.id.map('{:06d}'.format)
        return krx

    def update_comp_info(self):
        """종목코드를 company_info 테이블에 업데이트 한 후 딕셔너리에 저장"""
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)
        for idx in range(len(df)):
            self.codes[df['id'].values[idx]] = df['name'].values[idx]

        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    id = krx.id.values[idx]
                    name = krx.name.values[idx]
                    print('{}, {}'.format(id, name))
                    sql = f"INSERT INTO company_info (id, name, last_update)" \
                          f"VALUES ('{id}', '{name}', '{today}')" \
                          f"ON DUPLICATE KEY UPDATE id='{id}', last_update='{today}'"
                    curs.execute(sql)
                    self.codes[id] = name
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] #{idx + 1:04d} REPLACE INTO company_info " \
                          f"VALUES ({id}, {name}, {today})")
                self.conn.commit()
                print('')

    def read_naver(self, id, name, pages_to_fetch):
        """네이버에서 주식 시세를 읽어서 데이터프레임으로 반환"""
        try:
            url = f"http://finance.naver.com/item/sise_day.nhn?code={id}"
            html = BeautifulSoup(requests.get(url,
                                              headers={'User-agent': 'Mozilla/5.0'}).text, "lxml")
            pgrr = html.find("td", class_="pgRR")
            if pgrr is None:
                return None
            s = str(pgrr.a["href"]).split('=')
            lastpage = s[-1]
            df = pd.DataFrame()
            pages = min(int(lastpage), pages_to_fetch)
            for page in range(1, pages + 1):
                pg_url = '{}&page={}'.format(url, page)
                df = df.append(pd.read_html(requests.get(pg_url,
                                                         headers={'User-agent': 'Mozilla/5.0'}).text)[0])
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.
                      format(tmnow, name, id, page, pages), end="\r")
            df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff'
                , '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
            df['date'] = df['date'].replace('.', '-')
            df = df.dropna()
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close',
                                                                         'diff', 'open', 'high', 'low',
                                                                         'volume']].astype(int)
            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]
        except Exception as e:
            print('Exception occured :', str(e))
            return None
        return df

    def replace_into_db(self, df, num, id, name):
        """네이버에서 읽어온 주식 시세를 DB에 REPLACE"""
        with self.conn.cursor() as curs:
            for r in df.itertuples():
                sql = f"REPLACE INTO daily_price VALUES ('{id}', " \
                      f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close})"
                curs.execute(sql)

                sql = f"REPLACE INTO daily_volume VALUES ('{id}', " \
                      f"'{r.date}', {r.volume})"
                curs.execute(sql)
            self.conn.commit()
            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_' \
                  'price [OK]'.format(datetime.now().strftime('%Y-%m-%d' \
                                                              ' %H:%M'), num + 1, name, id, len(df)))

    def update_daily_price(self, pages_to_fetch):
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트"""
        for idx, id in enumerate(self.codes):
            df = self.read_naver(id, self.codes[id], pages_to_fetch)
            if df is None:
                continue
            self.replace_into_db(df, idx, id, self.codes[id])

    def execute_daily(self):
        """실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트"""
        self.update_comp_info()

        try:
            with open('config.json', 'r') as in_file:
                config = json.load(in_file)
                pages_to_fetch = config['pages_to_fetch']
        except FileNotFoundError:
            with open('config.json', 'w') as out_file:
                pages_to_fetch = 100
                config = {'pages_to_fetch': 1}
                json.dump(config, out_file)
        self.update_daily_price(pages_to_fetch)

        tmnow = datetime.now()
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]
        if tmnow.month == 12 and tmnow.day == lastday:
            tmnext = tmnow.replace(year=tmnow.year + 1, month=1, day=1,
                                   hour=17, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month + 1, day=1, hour=17,
                                   minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day + 1, hour=17, minute=0,
                                   second=0)
        tmdiff = tmnext - tmnow
        secs = tmdiff.seconds
        t = Timer(secs, self.execute_daily)
        print("Waiting for next update ({}) ... ".format(tmnext.strftime
                                                         ('%Y-%m-%d %H:%M')))
        t.start()


if __name__ == '__main__':
    dbu = DBUpdater()
    dbu.execute_daily()
