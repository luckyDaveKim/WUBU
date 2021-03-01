import win32com.client
import ctypes
from pywinauto import application
import os, time


class creon():

    cpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
    cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdutil')
    id = ""
    pwd = ""
    pwdcert = ""
    def __init__(self, config):
        pass

    def run_creon_service(self):
        os.system('taskkill /IM coStarter* /F /T')
        os.system('taskkill /IM CpStart* /F /T')
        os.system('taskkill /IM DibServer* /F /T')
        os.system('wmic process where "name like \'%coStarter%\'" call terminate')
        os.system('wmic process where "name like \'%CpStart%\'" call terminate')
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')

        time.sleep(5)
        app = application.Application()

        #'E:\STARTER\coStarter.exe /prj:cp '
        app.start("D:\WUBU\Creon\STARTER\coStarter.exe /prj:cp "
                "/id:{} /pwd:{} /pwdcert:{} /autostart".format(self.id, self.pwd, self.pwdcert))

        time.sleep(60)

    def check_creon_run(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print('Not Admin')
            return False

        if self.cpStatus.IsConnect == 0:
            print('Not Connect')
            return False

        return True

    def check_creon_system(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print('Not Admin')
            return False

        if self.cpStatus.IsConnect == 0:
            print('Not Connect')
            return False

        if self.cpTradeUtil.TradeInit(0) != 0:
            print('Not Trade Initialize')
            return False

        return True