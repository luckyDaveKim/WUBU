import win32com.client

# https://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=285&seq=81&page=6&searchString=&p=&v=&m=

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

objStockMst = win32com.client.Dispatch('CpSysDib.CpSvrNew7215A')

objStockMst.SetInputValue(0, ord('2'))
objStockMst.SetInputValue(1, ord('1'))
objStockMst.BlockRequest()

# 현재가 통신 및 통신 에러 처리
rqStatus = objStockMst.GetDibStatus()
rqRet = objStockMst.GetDibMsg1()
print("통신상태", rqStatus, rqRet)
if rqStatus != 0:
    exit()

print(objStockMst.GetHeaderValue(0))
print(objStockMst.GetHeaderValue(1))
print(objStockMst.GetHeaderValue(2))

for i in range(0, 10):
    item = {}
    item['종목코드'] = objStockMst.GetDataValue(0, i)
    item['순매도종목명'] = objStockMst.GetDataValue(1, i)
    item['순매도량'] = objStockMst.GetDataValue(2, i)
    item['순매도대금'] = objStockMst.GetDataValue(3, i)
    item['순매수종목코드'] = objStockMst.GetDataValue(4, i)
    item['순매수종목명'] = objStockMst.GetDataValue(5, i)
    item['순매수량'] = objStockMst.GetDataValue(6, i)
    item['순매수대금'] = objStockMst.GetDataValue(7, i)
    print(item)
