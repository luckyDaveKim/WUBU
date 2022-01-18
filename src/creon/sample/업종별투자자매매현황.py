import win32com.client

# https://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=72&page=1&searchString=%ec%97%85%ec%a2%85%eb%aa%85&p=&v=&m=

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

# 현재가 객체 구하기
objStockMst = win32com.client.Dispatch("DsCbo1.CpSvr7223")
objStockMst.SetInputValue(0, ord("3"))
objStockMst.SetInputValue(1, "001")
objStockMst.SetInputValue(2, ord("1"))
objStockMst.SetInputValue(3, ord("2"))
objStockMst.BlockRequest()

# 현재가 정보 조회
print(objStockMst.GetHeaderValue(0))
print(objStockMst.GetHeaderValue(1))

totcnt = 0
while True:
    objStockMst.BlockRequest()
    # 통신 및 통신 에러 처리
    rqStatus = objStockMst.GetDibStatus()
    rqRet = objStockMst.GetDibMsg1()
    print("통신상태", rqStatus, rqRet)
    if rqStatus != 0:
        break

    cnt = objStockMst.GetHeaderValue(1)
    totcnt += cnt

    for i in range(cnt):
        item = {}
        fixed = objStockMst.GetDataValue(18, i)
        # 잠정치는 일단 버린다
        if (fixed == ord('0')):
            continue

        item['업종명 / 시간 / 일자'] = objStockMst.GetDataValue(0, i)
        item['개인'] = objStockMst.GetDataValue(1, i)
        item['외국인'] = objStockMst.GetDataValue(2, i)
        item['기관'] = objStockMst.GetDataValue(3, i)
        item['금융투자'] = objStockMst.GetDataValue(4, i)
        item['보험'] = objStockMst.GetDataValue(5, i)
        item['투신'] = objStockMst.GetDataValue(6, i)
        item['은행'] = objStockMst.GetDataValue(7, i)
        item['기타금융'] = objStockMst.GetDataValue(8, i)
        item['연기금등'] = objStockMst.GetDataValue(9, i)
        item['기타법인'] = objStockMst.GetDataValue(10, i)
        item['기타외국인'] = objStockMst.GetDataValue(11, i)
        item['사모펀드'] = objStockMst.GetDataValue(12, i)
        item['국가, 지자체'] = objStockMst.GetDataValue(13, i)
        print(item)

    if (totcnt >= 10):
        break
    if (objStockMst.Continue == False):
        break
