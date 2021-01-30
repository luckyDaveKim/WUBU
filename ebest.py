from datetime import time

import pythoncom
import win32com.client as winAPI

STAND_BY = 0
RECEIVED = 1


class XASessionEvents:
    loginState = STAND_BY
    loginFlag = False

    def OnLogin(self, code, msg):
        if code == "0000":  # success code
            XASessionEvents.loginState = RECEIVED
            XASessionEvents.loginFlag = True
        print(msg)

    def OnDisconnect(self):
        XASessionEvents.loginFlag = False
        print("로그아웃")


class XAQueryEvents:
    query_state = STAND_BY

    def OnReceiveData(self, code):
        XAQueryEvents.query_state = RECEIVED

    def OnReceiveMessage(self, error, nMessageCode, szMessage):
        print(szMessage)


class Finance():
    SUCCESS = 1
    ERROR = -1
    TRANSACTION_REQUEST_EXCESS = -21
    resFileName = "E:\\eBEST\\xingAPI\\Res\\{0}.res"
    kospiCode = []
    kospiName = []
    kosdaqCode = []
    kosdaqName = []

    def __init__(self):
        self.__SERVER_PORT = 20001
        self.__SHOW_CERTIFICATE_ERROR_DIALOG = False
        self.__REPEATED_DATA_QUERY = 1

        self.__id = None
        self.__password = None
        self.__certificate_password = None
        self.__xa_session = None

    def login(self):
        # TODO DB로 변경
        with open("./user.txt") as f:
            lines = f.readlines()
            self.__id = lines[0].strip()
            self.__password = lines[1].strip()
            self.__certificate_password = lines[2].strip()
        pythoncom.CoInitialize()
        xa_session = winAPI.DispatchWithEvents("XA_Session.XASession", XASessionEvents)

        if xa_session.IsConnected() is True:
            xa_session.DisconnectServer()
        # demo.ebestsec.co.kr => 모의투자
        # hts.ebestsec.co.kr => 실투자
        xa_session.ConnectServer("hts.ebestsec.co.kr", self.__SERVER_PORT)
        xa_session.Login(self.__id, self.__password, self.__certificate_password, self.__SERVER_PORT,
                         self.__SHOW_CERTIFICATE_ERROR_DIALOG)
        while XASessionEvents.loginState is STAND_BY:
            pythoncom.PumpWaitingMessages()
        XASessionEvents.loginState = STAND_BY

        self.__xa_session = xa_session
        return self.SUCCESS

    def logout(self):
        if XASessionEvents.loginFlag:
            self.__xa_session.DisconnectServer()


    def kospiLoad(self):
        # 코스피 로드
        TR = "t8430"
        xa_query = winAPI.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        xa_query.ResFileName = self.resFileName.format(TR) #"E:\\eBEST\\xingAPI\\Res\\" + TR + ".res"
        print(xa_query.ResFileName)

        xa_query.SetFieldData("t8430InBlock", "gubun", 0, 1)

        while True:
            ret = xa_query.Request(False)
            """ Receiving error message, keep requesting until accepted """
            if ret is self.TRANSACTION_REQUEST_EXCESS:
                time.sleep(0.8)
            else:
                break
        """ Wait window's event message """
        while XAQueryEvents.query_state is STAND_BY:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.query_state = STAND_BY

        for idx in range(xa_query.GetBlockCount('t8430OutBlock')):
            self.kospiCode.append(xa_query.GetFieldData('t8430OutBlock', 'shcode', idx))
            self.kospiName.append(xa_query.GetFieldData('t8430OutBlock', 'hname', idx))

    def kosdaqLoad(self):
        # 코스닥 로드
        TR = "t8430"
        xa_query = winAPI.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        xa_query.ResFileName = self.resFileName.format(TR)  # "E:\\eBEST\\xingAPI\\Res\\" + TR + ".res"
        print(xa_query.ResFileName)

        xa_query.SetFieldData("t8430InBlock", "gubun", 0, 2)

        while True:
            ret = xa_query.Request(False)
            """ Receiving error message, keep requesting until accepted """
            if ret is self.TRANSACTION_REQUEST_EXCESS:
                time.sleep(0.8)
            else:
                break
        """ Wait window's event message """
        while XAQueryEvents.query_state is STAND_BY:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.query_state = STAND_BY

        for idx in range(xa_query.GetBlockCount('t8430OutBlock')):
            self.kosdaqCode.append(xa_query.GetFieldData('t8430OutBlock', 'shcode', idx))
            self.kosdaqName.append(xa_query.GetFieldData('t8430OutBlock', 'hname', idx))

    def reviewAccount(self):
        accountNum = self.__xa_session.GetAccountListCount()
        for i in range(accountNum):
            account = self.__xa_session.GetAccountList(i)
            return account

    def getPrice(self, searchData):
        print(1)
        koreaAllCode = self.kospiCode + self.kosdaqCode
        koreaAllName = self.kospiName + self.kosdaqName
        code = None
        if searchData.isdigit():
            code = searchData
        else:
            try:
                code = koreaAllCode[koreaAllName.index(searchData)]
            except ValueError:
                return self.ERROR
        TR = "t1101"
        xa_query = winAPI.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)

        xa_query.ResFileName = self.resFileName.format(TR)  # "E:\\eBEST\\xingAPI\\Res\\" + TR + ".res"
        print(xa_query.ResFileName)

        xa_query.SetFieldData("t1101InBlock", "shcode", 0, code)

        while True:
            ret = xa_query.Request(False)
            if ret is self.TRANSACTION_REQUEST_EXCESS:
                time.sleep(0.8)
            else:
                break

        while XAQueryEvents.query_state is STAND_BY:
            pythoncom.PumpWaitingMessages()
        XAQueryEvents.query_state = STAND_BY

        name = xa_query.GetFieldData('t1101OutBlock', 'hname', 0)
        price = xa_query.GetFieldData('t1101OutBlock', 'price', 0)
        return price


if __name__ == "__main__":
    # TEST

    finance = Finance()
    if finance.login() == Finance.SUCCESS:
      print ("SUCCESS")

    finance.reviewAccount()

    finance.kospiLoad()
    print(finance.kospiCode)
    print(finance.kospiName)
    finance.kosdaqLoad()

    print(finance.kosdaqCode)
    print(finance.kosdaqName)

    print(finance.getPrice("삼성전자"))
    print(finance.getPrice("005930"))

    finance.logout()