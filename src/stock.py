import sys

import pymysql

from kiwoom import Kiwoom, QApplication

app = QApplication(sys.argv)
kiwoom = Kiwoom()
kiwoom.comm_connect()

conn = pymysql.connect(host='localhost', user='wubu', password='wubudnflqnwkehlwk', db='wubu', charset='utf8')
cur = conn.cursor()


kiwoom.set_input_value("종목코드", "005930")
kiwoom.set_input_value("기준일자", '20210129')
kiwoom.set_input_value("수정주가구분", 1)
kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "1999")

# '005930'
# print(kiwoom.get_master_stock_state('005930'))
    # sql = "INSERT INTO markets (market_code, market_name) VALUES ('{market_code}', '{market_name}')"
    # sql = sql.format(market_code=market_code, market_name=market_name)
    # try:
    #     cur.execute(sql)
    # except Exception as e:
    #     print(e)
    #     print(sql)

conn.commit()

conn.close()