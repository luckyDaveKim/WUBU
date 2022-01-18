import win32com.client

#https://money2.creontrade.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=11&page=1&searchString=CpUtil.CpCodeMgr&p=8841&v=8643&m=9505

# 연결 여부 체크
from db_manager import DBManager

objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

objStockMst = win32com.client.Dispatch('CpUtil.CpCodeMgr')
codeList = objStockMst.GetIndustryList()  # 증권 산업 업종 리스트
codeList2 = objStockMst.GetKosdaqIndustry1List()  # 코스닥산업별코드리스트를반환한다.
allcodelist = codeList + codeList2
print("\n### 증권수 #", len(codeList))
print("\n### 코스닥수 #", len(codeList2))
print("\n### 업종 코드 #", len(allcodelist))

items = []
for code in allcodelist:
    name = objStockMst.CodeToName(code)

    item = {'code': code, 'name': name}
    items.append(item)

    # print(code, name)

db_manger = DBManager()
db_manger.insert_sectors_info(items)