import win32com.client

# https://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=285&seq=143&page=3&searchString=&p=&v=&m=

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

objStockMst = win32com.client.Dispatch('CpSysDib.CpSvrNew7216')
objStockMst.SetInputValue(0, '035720')

# 현재가 통신 및 통신 에러 처리
rqStatus = objStockMst.GetDibStatus()
rqRet = objStockMst.GetDibMsg1()
print("통신상태", rqStatus, rqRet)
if rqStatus != 0:
    exit()

print('종목코드', objStockMst.GetHeaderValue(0))
print('카운트', objStockMst.GetHeaderValue(1))
print('조회일자', objStockMst.GetHeaderValue(2))

item = {}
item['일자'] = objStockMst.GetDataValue(0, 0)
item['종가'] = objStockMst.GetDataValue(1, 0)
item['전일대비flag'] = objStockMst.GetDataValue(2, 0)
item['전일대비'] = objStockMst.GetDataValue(3, 0)
item['전일대비율'] = objStockMst.GetDataValue(4, 0)
item['거래량'] = objStockMst.GetDataValue(5, 0)
item['기관매매'] = objStockMst.GetDataValue(6, 0)
item['기관매매누적'] = objStockMst.GetDataValue(7, 0)
item['외국인순매매'] = objStockMst.GetDataValue(8, 0)
item['외국인지분율'] = objStockMst.GetDataValue(9, 0)
print(item)
