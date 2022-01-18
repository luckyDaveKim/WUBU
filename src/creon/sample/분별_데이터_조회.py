import pandas as pd
import win32com.client

from db_manager import DBManager

# https://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=102&page=1&searchString=CpSysDib.StockChart&p=&v=&m=

db_manger = DBManager()

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

objStockMst = win32com.client.Dispatch("CpSysDib.StockChart")

objStockMst.SetInputValue(0, 'A035720')  # 종목코드
objStockMst.SetInputValue(1, ord('2'))  # 요청구분 (1:기간, 2:개수)
objStockMst.SetInputValue(4, 200)  # 요청개수
objStockMst.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 요청필드 (날짜, 시간, 시가, 고가, 저가, 종가, 거래량)
objStockMst.SetInputValue(6, ord('m'))  # 차트구분 (D:일, W:주, M:월, m:분, T:틱)

totcnt = 0
MAX_COUNT = 200
while True:
    objStockMst.BlockRequest()
    # 통신 및 통신 에러 처리
    rqStatus = objStockMst.GetDibStatus()
    rqRet = objStockMst.GetDibMsg1()
    print("통신상태", rqStatus, rqRet)
    if rqStatus != 0:
        break

    company_id = objStockMst.GetHeaderValue(0)[1:]
    filed_cnt = objStockMst.GetHeaderValue(1)
    filed_names = objStockMst.GetHeaderValue(2)
    cnt = objStockMst.GetHeaderValue(3)
    totcnt += cnt

    print('GET DATA >>>>>>>>>>>>>>> ', totcnt)

    items = []
    for i in range(cnt):
        item = {}
        for j in range(filed_cnt):
            item[filed_names[j]] = objStockMst.GetDataValue(j, i)

        items.append(item)

    db_manger.insert_minutely_price(items, company_id)
    db_manger.insert_minutely_volume(items, company_id)

    if (objStockMst.Continue == False):
        break
    if totcnt >= MAX_COUNT:
        break
