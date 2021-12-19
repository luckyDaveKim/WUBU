import calendar
import json
import pandas as pd
import pymysql
import requests
import sys
from Query import Query
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Timer


class DBUpdater:
    __conn = None
    __query = None

    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.__conn = self.__get_init_db()
        self.__query = Query()

        self.__init_tables()

        self.__companies_id_to_name = dict()

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

    def __execute(self, query):
        self.__conn.cursor().execute(query)
        self.__conn.commit()

    def __init_tables(self):
        self.__execute(self.__query.init_company_info())
        self.__execute(self.__query.init_daily_price())
        self.__execute(self.__query.init_daily_volume())

    def get_companies(self):
        """KRX로부터 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드': 'id', '회사명': 'name'})
        krx.id = krx.id.map('{:06d}'.format)
        return krx

    def update_comp_info(self):
        """종목코드를 company_info 테이블에 업데이트 한 후 딕셔너리에 저장"""
        df = pd.read_sql(self.__query.select_company_info(), self.__conn)
        for index in range(len(df)):
            id = df['id'].values[index]
            name = df['name'].values[index]
            self.__companies_id_to_name[id] = name

        with self.__conn.cursor() as curs:
            curs.execute(self.__query.get_last_update_date())
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')
            needed_update = rs[0] == None or rs[0].strftime('%Y-%m-%d') < today
            if needed_update:
                companies = self.get_companies()
                for index in range(len(companies)):
                    id = companies.id.values[index]
                    name = companies.name.values[index]
                    print(f'INSERT company_info; id="{id}", name="{name}"')
                    curs.execute(self.__query.insert_company_info(id, name, today))
            self.__conn.commit()

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
                print(f'[{tmnow}] {name} ({id}) : {page:04d}/{pages:04d} pages are downloading...', end="\r")
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

    def update_daily_price(self, pages_to_fetch):
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트"""
        for idx, id in enumerate(self.__companies_id_to_name):
            df = self.get_daily_data(id, self.__companies_id_to_name[id], pages_to_fetch)
            if df is None:
                continue
            self.update_daily_price_and_volume(df, idx, id, self.__companies_id_to_name[id])

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

        print(f'Waiting for next update ({tmnext.strftime("%Y-%m-%d %H:%M")}) ... ')

        tmdiff = tmnext - tmnow
        secs = tmdiff.seconds
        t = Timer(secs, self.execute_daily)
        t.start()


if __name__ == '__main__':
    dbu = DBUpdater()
    dbu.execute_daily()
