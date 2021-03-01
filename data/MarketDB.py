import re
from datetime import datetime

import json
import pandas
import pymysql


class MarketDB:
    def __init__(self):
        self.__conn = self.__get_connection()
        self.__codes = self.__load_codes()

    @staticmethod
    def __get_connection():
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
        return pymysql.connect(host=host, user=user,
                               password=password, db=db)

    def __load_codes(self):
        data = self.__get_data('SELECT * FROM company_info')
        codes = {}
        for i in range(len(data)):
            codes[data['code'].values[i]] = data['company'].values[i]
        return codes

    def __get_data(self, sql):
        return pandas.read_sql(sql, self.__conn)

    @staticmethod
    def _parse_date(date):
        date_token = re.split('\D+', date.strip())
        year = int(date_token[0])
        month = int(date_token[1])
        day = int(date_token[2])
        return datetime(year, month, day).strftime('%Y-%m-%d')

    def get_codes(self):
        return self.__codes

    def get_code(self, code):
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

    def get_daily_price(self, code, start_date, end_date=None):
        code = self.get_code(code)
        start_date = self._parse_date(start_date)
        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')
        end_date = self._parse_date(end_date)

        sql = f'SELECT * FROM daily_price WHERE code = "{code}" and date BETWEEN "{start_date}" AND "{end_date}"'
        data = self.__get_data(sql)
        data.index = data['date']
        return data
