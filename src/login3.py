import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *

class KiwoomLogin:
    def login(self, kiwoom):
        kiwoom.dynamicCall("CommConnect()")
        kiwoom.OnEventConnect.connect(self.login_event)

    def login_event(self, error):
        if error == 0:
            print('로그인 성공')
        else:
            print('로그인 실패 Code : ' + str(error))

class KiwoomSearch:
    def search(self, kiwoom):
        print('조회 시도')
        # result = kiwoom.dynamicCall('GetCodeListByMarket(QString)', str(0))
        result = kiwoom.dynamicCall('GetMasterCodeName(QString)', '005930')
        print(result)


class KiwoomAPI(QMainWindow, KiwoomLogin, KiwoomSearch):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KiwoomAPI")
        self.setGeometry(300, 300, 300, 300)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        KiwoomLogin.login(self, self.kiwoom)

        btn2 = QPushButton("Check state", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)

        btn3 = QPushButton("Check state", self)
        btn3.move(20, 120)
        btn3.clicked.connect(self.btn3_clicked)

    def btn2_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")

    def btn3_clicked(self):
        KiwoomSearch.search(self, self.kiwoom)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoomApi = KiwoomAPI()
    kiwoomApi.show()
    app.exec_()