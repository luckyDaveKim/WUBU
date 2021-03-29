import win32com.client
import ctypes


class Creon():
    def __init__(self):
        self.__validateAdmin()
        self.codeManager = self.CodeManager()
        self.cybosManager = self.CybosManager()
        self.tradeManager = self.TradeManager()

    def __validateAdmin(self):
        # 프로세스가 관리자 권한으로 실행 여부
        if not ctypes.windll.shell32.IsUserAnAdmin():
            raise Exception('일반권한으로 실행됨. 관리자 권한으로 실행해 주세요')

    class CodeManager():
        def __init__(self):
            self.__controller = win32com.client.Dispatch('CpUtil.CpCodeMgr')

        def codeToName(self, code):
            return self.__controller.CodeToName(code)

        def getGroupCodeList(self, groupCode):
            return self.__controller.GetGroupCodeList(groupCode)

    class CybosManager():
        def __init__(self):
            self.__controller = win32com.client.Dispatch('CpUtil.CpCybos')

        def __validateConnect(self):
            if self.__controller.IsConnect == 0:
                raise Exception('Cybos가 정상적으로 연결되지 않았습니다.')

    class TradeManager():
        def __init__(self):
            self.__controller = win32com.client.Dispatch('CpTrade.CpTdUtil')

        def __validateInit(self):
            if self.__controller.TradeInit(0) != 0:
                raise Exception('Trade가 정상적으로 초기화되지 않았습니다.')
