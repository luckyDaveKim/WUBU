import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import pandas as pd
class KiwoomAPIWindow(QMainWindow):
    def __init__(self, connect=1):
        super().__init__()
        self.title = 'AutoTrader'
        self.left = 50
        self.top = 50
        self.width = 640
        self.height = 480
        self.initUI()
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        if connect == 1:
            # API 연결
            self.kiwoom.dynamicCall("CommConnect()")
        # API 연결 되었는지를 Status Bar에 출력
        self.kiwoom.OnEventConnect.connect(self.login_event)
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # 라벨 생성
        label_market = QLabel('장 선택 ', self)
        label_market.move(10, 70)
        # 콤보 박스 생성
        self.cbox_market = QComboBox(self)
        self.cbox_market.setGeometry(100, 70, 150, 32)
        self.cbox_market.setObjectName(("box"))
        self.cbox_market.addItem("장내", userData=0)
        self.cbox_market.addItem("코스닥", userData=10)
        self.cbox_market.addItem("코넥스", userData=50)
        # 버튼 생성
        btn_market = QPushButton('장 리스트 가져오기', self)
        btn_market.setToolTip('0: 장내, 10: 코스닥, 50: 코넥스 등등등 Spec 참조 ')
        btn_market.resize(200, 32)
        btn_market.move(300, 70)
        btn_market.clicked.connect(self.on_click_market)
        self.show()
    def login_event(self, error):
        if error == 0:
            strs = '로그인 성공 Code : ' + str(error)
            self.statusBar().showMessage(strs)
        else:
            strs = '로그인 실패 Code : ' + str(error)
            self.statusBar().showMessage(strs)
    def on_click_market(self):
        print(self.cbox_market.currentText(), ' ',self.cbox_market.currentData())
        # GetCodeListByMarket 으로 종목코드 요청
        result = self.kiwoom.dynamicCall('GetCodeListByMarket(QString)', str(self.cbox_market.currentData()))
        code_list = result.split(';')
        data_list = []
        for code in code_list:
            name = self.kiwoom.dynamicCall('GetMasterCodeName(QString)', code)
            data_list.append([name, code])
        # 데이터 프레임으로 만들기
        df = pd.DataFrame(data_list, columns=['회사명', '종목코드'])
        print(df.head())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    kaWindow = KiwoomAPIWindow()
