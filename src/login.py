import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self, login=0):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 300)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        self.loginResult = 999

        self.statusBar().showMessage(str(self.kiwoom.dynamicCall("GetConnectState()")))

        if login == 0:
            self.loginResult = self.kiwoom.dynamicCall("CommConnect()")

        self.kiwoom.OnEventConnect.connect(self.login_event)

        btn1 = QPushButton("Login", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton("Check state", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)

        btn3 = QPushButton("Check state", self)
        btn3.move(20, 120)
        btn3.clicked.connect(self.btn3_clicked)


    def login_event(self, error):
        if error == 0:
            strs = '로그인 성공 Code : ' + str(error)
            self.statusBar().showMessage(strs)
        else:
            strs = '로그인 실패 Code : ' + str(error)
            self.statusBar().showMessage(strs)

    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")

    def btn2_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")

    def btn3_clicked(self):
        self.statusBar().showMessage(str(self.loginResult))
        # self.statusBar().showMessage(self.kiwoom.dynamicCall("GetMasterCodeName(005930)"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()