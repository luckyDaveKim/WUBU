import win32com.client

# 연결 여부 체크
from db_manager import DBManager

objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

# 현재가 객체 구하기
objStockMst = win32com.client.Dispatch("Dscbo1.StockIndexIR")
objStockMst.SetInputValue(0, "U001")

DATE = '2021-09-24'
items = []
while True:
    objStockMst.BlockRequest()
    # 현재가 통신 및 통신 에러 처리
    rqStatus = objStockMst.GetDibStatus()
    if rqStatus != 0:
        break

    # 현재가 정보 조회
    print(objStockMst.GetHeaderValue(0))
    print(objStockMst.GetHeaderValue(1))
    print(objStockMst.GetHeaderValue(2))

    cnt = objStockMst.GetHeaderValue(1)

    for i in range(cnt):
        item = {}
        item['code'] = objStockMst.GetHeaderValue(0)
        item['시간'] = '{} {}00'.format(DATE, objStockMst.GetDataValue(0, i))
        item['지수'] = objStockMst.GetDataValue(1, i)
        item['전일대비'] = objStockMst.GetDataValue(2, i)
        item['거래량'] = objStockMst.GetDataValue(3, i)    # 일의 단위
        item['거래대금'] = '{}000000'.format(objStockMst.GetDataValue(4, i))   # 백만 단위

        items.append(item)

        # print(item)

    if (objStockMst.Continue == False):
        print('objStockMst.Continue break', objStockMst.Continue)
        break

db_manger = DBManager()
db_manger.insert_sectors_minutely_index(items)
db_manger.insert_sectors_minutely_volume(items)
db_manger.insert_sectors_minutely_price(items)