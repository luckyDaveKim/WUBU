import win32com.client

# https://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=285&seq=141&page=3&searchString=&p=&v=&m=

g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

objStockMst = win32com.client.Dispatch('Dscbo1.CpSvr8091')

codeList = g_objCodeMgr.GetStockListByMarket(1)  # 거래소
codeList2 = g_objCodeMgr.GetStockListByMarket(2)  # 코스닥
allcodelist = codeList + codeList2
print('전 종목 코드 %d, 거래소 %d, 코스닥 %d' % (len(allcodelist), len(codeList), len(codeList2)))

print(allcodelist)

# objMarket = CpMarketEye()
# rqCodeList = []
# for i, code in enumerate(allcodelist):
#     rqCodeList.append(code)
#     if len(rqCodeList) == 200:
#         objMarket.Request(rqCodeList, self.dataInfo)
#         rqCodeList = []
#         continue
# # end of for
#
# if len(rqCodeList) > 0:
#     objMarket.Request(rqCodeList, self.dataInfo)
