import re
from datetime import datetime

import pandas
import pymysql


class MarketDB:
    def __init__(self):
        self.__conn = self.__get_connection()
        self.__codes = self.__load_codes()

    @staticmethod
    def __get_connection():
        return pymysql.connect(host='localhost', user='root', password='root', db='wubu', charset='utf8')

    def __load_codes(self):
        data = self.__get_data('SELECT * FROM markets')
        codes = {}
        for i in range(len(data)):
            codes[data['market_code'].values[i]] = data['market_name'].values[i]
        return codes

    def __get_data(self, sql):
        return pandas.read_sql(sql, self.__conn)

    def __get_code(self, code):
        code_keys = list(self.__codes.keys())
        code_values = list(self.__codes.values())

        if code in code_keys:
            pass
        elif code in code_values:
            idx = code_values.index(code)
            code = code_keys[idx]
        else:
            print(f"ValueError: Code({code}) doesn't exist.")

        return code

    @staticmethod
    def _parse_date(date):
        date_token = re.split('\D+', date.strip())
        year = int(date_token[0])
        month = int(date_token[1])
        day = int(date_token[2])
        hour = int(date_token[3])
        min = int(date_token[4])
        sec = int(date_token[5])
        return datetime(year, month, day, hour, min, sec).strftime('%Y-%m-%d %H:%M:%S')

    def get_minly_price(self, code, start_date, end_date):
        code = self.__get_code(code)
        start_date = self._parse_date(start_date)
        end_date = self._parse_date(end_date)

        sql = f'SELECT * FROM market_history_per_minute WHERE market_code = "{code}" and datetime BETWEEN "{start_date}" AND "{end_date}"'
        data = self.__get_data(sql)
        data.index = data['datetime']
        return data
