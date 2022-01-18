import json
import re
import sys
from datetime import datetime

import pymysql


class DBManager:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root', password='root', db='investar')

        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS minutely_price (
                company_id VARCHAR(20),
                datetime DATETIME,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                PRIMARY KEY (company_id, datetime))
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS minutely_volume (
                company_id VARCHAR(20),
                datetime DATETIME,
                volume BIGINT(20),
                PRIMARY KEY (company_id, datetime))
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS minutely_exchange_rate (
                datetime DATETIME,
                rate FLOAT(20, 2),
                PRIMARY KEY (datetime))
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS daily_exchange_rate (
                date DATE,
                rate FLOAT(20, 2),
                PRIMARY KEY (date))
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS sectors_info (
                sectors_id VARCHAR(20),
                name VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (sectors_id))
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS sectors_minutely_index (
                sectors_id VARCHAR(20),
                datetime DATETIME,
                open FLOAT(20, 2),
                high FLOAT(20, 2),
                low FLOAT(20, 2),
                close FLOAT(20, 2),
                PRIMARY KEY (sectors_id, datetime))
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS sectors_minutely_volume (
                sectors_id VARCHAR(20),
                datetime DATETIME,
                amount BIGINT(20),
                PRIMARY KEY (sectors_id, datetime))
            """
            curs.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS sectors_minutely_price (
                sectors_id VARCHAR(20),
                datetime DATETIME,
                amount BIGINT(20),
                PRIMARY KEY (sectors_id, datetime))
            """
            curs.execute(sql)

        self.conn.commit()

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def insert_minutely_price(self, items, company_id):
        try:
            with self.conn.cursor() as curs:
                for item in items:
                    sql = f"REPLACE INTO minutely_price VALUES ('{company_id}', STR_TO_DATE('{str(item['날짜']) + str(item['시간']).zfill(4)}', '%Y%m%d%H%i'), {item['시가']}, {item['고가']}, {item['저가']}, {item['종가']})"
                    print(sql)
                    curs.execute(sql)
                self.conn.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])

        print(
            '[{}] {} : {} rows > REPLACE INTO minutely_price [OK]'.format(
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                company_id, len(items))
        )

    def insert_minutely_volume(self, items, company_id):
        try:
            with self.conn.cursor() as curs:
                for item in items:
                    sql = f"REPLACE INTO minutely_volume VALUES ('{company_id}', STR_TO_DATE('{str(item['날짜']) + str(item['시간']).zfill(4)}', '%Y%m%d%H%i'), {item['거래량']})"
                    print(sql)
                    curs.execute(sql)
                self.conn.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])

        print(
            '[{}] {} : {} rows > REPLACE INTO minutely_price [OK]'.format(
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                company_id, len(items))
        )

    # def insert_minutely_exchange_rate(self, items):
    #     # items[0] : {'datetime', 'rate'}
    #     try:
    #         with self.conn.cursor() as curs:
    #             for item in items:
    #                 datetime = item['datetime']
    #                 rate = item['rate']
    #
    #                 sql = f"REPLACE INTO minutely_exchange_rate VALUES (STR_TO_DATE('{datetime}', '%Y-%m-%d %H%i%s'), {rate})"
    #                 print(sql)
    #                 curs.execute(sql)
    #             self.conn.commit()
    #     except:
    #         print("Unexpected error:", sys.exc_info()[0])

    def insert_minutely_exchange_rate(self, date, df):
        # date (YYYY-MM-DD)
        # for r in df.itertuples():
        # r[1] : time (hh:mm:ss)
        # r[2] : rate
        try:
            with self.conn.cursor() as curs:
                for r in df.itertuples():
                    time = r[1]
                    datetime = '{} {}'.format(date, time)
                    rate = r[2]

                    sql = f"REPLACE INTO minutely_exchange_rate VALUES (STR_TO_DATE('{datetime}', '%Y-%m-%d %H:%i:%s'), {rate})"
                    print(sql)
                    curs.execute(sql)
                self.conn.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def insert_daily_exchange_rate(self, df):
        # for r in df.itertuples():
        # r[1] : date (YYYY.MM.DD)
        # r[2] : rate
        try:
            with self.conn.cursor() as curs:
                for r in df.itertuples():
                    date = r[1]
                    rate = r[2]

                    sql = f"REPLACE INTO daily_exchange_rate VALUES (STR_TO_DATE('{date}', '%Y.%m.%d'), {rate})"
                    print(sql)
                    curs.execute(sql)
                self.conn.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def insert_sectors_info(self, items):
        # items[0] : {'code', 'name'}
        try:
            with self.conn.cursor() as curs:
                today = datetime.today().strftime('%Y-%m-%d')
                for item in items:
                    code = item['code']
                    name = item['name']
                    sql = f"REPLACE INTO sectors_info VALUES ('{code}', '{name}', '{today}')"
                    print(sql)
                    curs.execute(sql)
                self.conn.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def insert_sectors_minutely_index(self, items, sectors_id):
        # items[0] : {날짜(YYYYMMDD), 시간(hhmm), 시가, 고가, 저가, 종가, 거래량, 거래대금}
        try:
            with self.conn.cursor() as curs:
                for item in items:
                    datetime = '{}{}'.format(item['날짜'], str(item['시간']).zfill(4))
                    open = float('{:.2f}'.format(item['시가']))
                    high = float('{:.2f}'.format(item['고가']))
                    low = float('{:.2f}'.format(item['저가']))
                    close = float('{:.2f}'.format(item['종가']))
                    sql = f"REPLACE INTO sectors_minutely_index VALUES ('{sectors_id}', STR_TO_DATE('{datetime}', '%Y%m%d%H%i'), {open}, {high}, {low}, {close})"
                    # print(sql)
                    curs.execute(sql)
                self.conn.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def insert_sectors_minutely_volume(self, items, sectors_id):
        # items[0] : {날짜(YYYYMMDD), 시간(hhmm), 시가, 고가, 저가, 종가, 거래량, 거래대금}
        try:
            with self.conn.cursor() as curs:
                for item in items:
                    datetime = '{}{}'.format(item['날짜'], str(item['시간']).zfill(4))
                    volume = item['거래량']
                    sql = f"REPLACE INTO sectors_minutely_volume VALUES ('{sectors_id}', STR_TO_DATE('{datetime}', '%Y%m%d%H%i'), {volume})"
                    # print(sql)
                    curs.execute(sql)
                self.conn.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def insert_sectors_minutely_price(self, items, sectors_id):
        # items[0] : {날짜(YYYYMMDD), 시간(hhmm), 시가, 고가, 저가, 종가, 거래량, 거래대금}
        try:
            with self.conn.cursor() as curs:
                for item in items:
                    datetime = '{}{}'.format(item['날짜'], str(item['시간']).zfill(4))
                    amount = item['거래대금']
                    sql = f"REPLACE INTO sectors_minutely_price VALUES ('{sectors_id}', STR_TO_DATE('{datetime}', '%Y%m%d%H%i'), {amount})"
                    # print(sql)
                    curs.execute(sql)
                self.conn.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
