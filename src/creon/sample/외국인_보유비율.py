import win32com.client

# https://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=102&page=1&searchString=CpSysDib.StockChart&p=8841&v=8643&m=9505

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

objStockMst = win32com.client.Dispatch('CpSysDib.StockChart')
objStockMst.SetInputValue(0, 'A005930')
objStockMst.SetInputValue(1, ord('1'))
# objStockMst.SetInputValue(2, '20040131')
objStockMst.SetInputValue(3, '20210823')
# objStockMst.SetInputValue(4, 10)
objStockMst.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8, 9, 12, 13, 14, 15, 16, 17, 20, 21])

totcnt = 0
while True:
    objStockMst.BlockRequest()
    # 통신 및 통신 에러 처리
    rqStatus = objStockMst.GetDibStatus()
    rqRet = objStockMst.GetDibMsg1()
    print("통신상태", rqStatus, rqRet)
    if rqStatus != 0:
        break

    print('종목코드', objStockMst.GetHeaderValue(0))
    print('필드개수', objStockMst.GetHeaderValue(1))
    fieldSize = objStockMst.GetHeaderValue(1)
    print('필드명의배열', objStockMst.GetHeaderValue(2))
    fields = objStockMst.GetHeaderValue(2)
    print('수신개수', objStockMst.GetHeaderValue(3))
    cnt = objStockMst.GetHeaderValue(3)
    totcnt += cnt

    for i in range(cnt):
        item = {}
        for j in range(fieldSize):
            item[fields[j]] = objStockMst.GetDataValue(j, i)
        print(item)

    if (totcnt >= 10):
        break
    if (objStockMst.Continue == False):
        break