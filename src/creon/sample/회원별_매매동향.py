import win32com.client

#https://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=285&seq=141&page=3&searchString=&p=&v=&m=

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

objStockMst = win32com.client.Dispatch('Dscbo1.CpSvr8091')

# '1'외국계전체
# '3'회원사 + 종목전체
# '4'회원사선택 + 단일종목
# '5'단일종목+외국계전체
# '7'복수종목+외국계전체
# '8'복수종목+회원사
objStockMst.SetInputValue(0, ord('1'))
# objStockMst.SetInputValue(2, 'A005930')

totcnt = 0
while True:
    objStockMst.BlockRequest()
    # 통신 및 통신 에러 처리
    rqStatus = objStockMst.GetDibStatus()
    rqRet = objStockMst.GetDibMsg1()
    print("통신상태", rqStatus, rqRet)
    if rqStatus != 0:
        break

    cnt = objStockMst.GetHeaderValue(0)
    totcnt += cnt
    for i in range(cnt):
        item = {}
        item['시간'] = objStockMst.GetDataValue(0, i)
        item['회원사명'] = objStockMst.GetDataValue(1, i)
        item['종목코드'] = objStockMst.GetDataValue(2, i)
        item['종목명'] = objStockMst.GetDataValue(3, i)
        item['매도/매수'] = objStockMst.GetDataValue(4, i)
        item['매수/매도량'] = objStockMst.GetDataValue(5, i)
        item['순매수'] = objStockMst.GetDataValue(6, i)
        item['순매수부호'] = objStockMst.GetDataValue(7, i)
        item['상태구분'] = objStockMst.GetDataValue(8, i)
        item['현재가등락율'] = objStockMst.GetDataValue(9, i)
        item['외국계전체누적순매수'] = objStockMst.GetDataValue(10, i)
        print(item)

    if objStockMst.Continue == False:
        break
    if totcnt > 20:
        break
