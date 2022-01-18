import win32com.client

# https://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=285&seq=141&page=3&searchString=&p=&v=&m=

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
objStockMst = win32com.client.Dispatch("CpSysDib.MarketEye")

# 0:종목코드(string)
# 1:시간( ulong) - hhmm
# 4:현재가(long or float)
# 5:시가(long or float)
# 6:고가(long or float)
# 7:저가(long or float)
# 10:거래량( ulong)
# 20:총상장주식수(ulonglong) - 단위:주
# 21:외국인보유비율(float)
# 62:외국인순매매(long) - 단위:주
# 71:자본금(ulonglong)- 단위:백만
# 73:배당률(float)
# 74:배당수익률(float)
rqField = [0, 1, 4, 5, 6, 7, 10, 20, 21, 62, 71, 73, 74]  # 요청 필드

objStockMst.SetInputValue(0, rqField)  # 요청 필드
objStockMst.SetInputValue(1, ['A005930', 'A003540'])
objStockMst.BlockRequest()

# 현재가 통신 및 통신 에러 처리
rqStatus = objStockMst.GetDibStatus()
rqRet = objStockMst.GetDibMsg1()
print("통신상태", rqStatus, rqRet)
if rqStatus != 0:
    exit()

# print(objStockMst.GetHeaderValue(0))
# print(objStockMst.GetHeaderValue(1))
# print(objStockMst.GetHeaderValue(2))

valSize = objStockMst.GetHeaderValue(0)
valNames = objStockMst.GetHeaderValue(1)
cnt = objStockMst.GetHeaderValue(2)

for i in range(cnt):
    item = {}
    for j in range(valSize):
        item[valNames[j]] = objStockMst.GetDataValue(j, i)
    print(item)
