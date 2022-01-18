import sys
import threading

import matplotlib
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


from data import MarketDB

from mplfinance.original_flavor import candlestick_ohlc
from MACD import MACD
from OHLC import OHLC


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__mk = MarketDB.MarketDB()
        self.__dfs = {}
        self.__initUI()
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        self.__stopBtnOnClicked()
        event.accept()

    def __initUI(self):
        self.__drawChart()
        self.__scanBtn()
        self.__stopBtn()
        self.__comboBox()

        self.setWindowTitle('Dave')
        self.resize(500, 550)
        self.show()

    def __drawChart(self):
        self.main_widget = QWidget()
        # self.setCentralWidget(self.main_widget)
        canvas = FigureCanvas(Figure(figsize=(7, 3)))
        vbox = QVBoxLayout(self.main_widget)
        vbox.addWidget(canvas)
        self.addToolBar(NavigationToolbar(canvas, self))

        self.ax = canvas.figure.subplots()
        self.ax.plot([0, 1, 2], [1, 5, 3], '-')

        # matplotlib.rcParams['font.family'] = "Malgun Gothic"
        # matplotlib.rcParams['axes.unicode_minus'] = False
        # plt.figure(figsize=(9, 7))
        # plt.show()

    def __statusBar(self):
        self.statusBar().showMessage('Ready')

    def __scanBtn(self):
        btn1 = QPushButton('Scan', self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.__scanBtnOnClicked)

    def __scanBtnOnClicked(self):
        self.statusBar().showMessage("Scan Start")
        self.__cb.clear()
        self.__dfs.clear()
        t = threading.Thread(target=self.__scan)
        t.start()

    def __scan(self):
        self.__scanRunning = True
        mk = MarketDB.MarketDB()
        codes = mk.get_codes().values()
        for code in codes:
            if not self.__scanRunning:
                print('break')
                break

            df = mk.get_daily_price(code, '2018-08-01')
            macd = MACD(df)
            trading_points = macd.get_trading_points()
            if len(trading_points) == 0:
                continue

            if trading_points[-1].get("x") >= mdates.date2num(np.datetime64("2021-02-18")) and \
                    trading_points[-1].get("trading") == "buy":
                self.__cb.addItem(code)
                self.__dfs[code] = df
                self.statusBar().showMessage(f"Found {code}")
        self.__scanRunning = False
        self.statusBar().showMessage("Scan End")

    def __stopBtn(self):
        stopBtn = QPushButton('Stop', self)
        stopBtn.move(200, 20)
        stopBtn.clicked.connect(self.__stopBtnOnClicked)

    def __stopBtnOnClicked(self):
        print('stop')
        self.__scanRunning = False

    def __comboBox(self):
        self.__cb = QComboBox(self)
        self.__cb.move(20, 100)
        self.__cb.activated[str].connect(self.__comboBoxOnActivated)
        self.__cb.addItem('고려제강')
        self.__cb.addItem('삼성전자')

    def __comboBoxOnActivated(self, code):
        self.statusBar().showMessage(f"Find {code}")

        df = self.__mk.get_daily_price(code, '2018-08-01')
        self.__openChart(code, df)
        # threading.Thread(target=self.__openChart, args=(code, df)).start()
        # threading.Thread(target=self.__openChart, args=(code, self.__dfs[code])).start()

    def __openChart(self, code, df):
        # QDialog 세팅
        ohlc = OHLC(df)
        macd = MACD(df)

        plt.clf()
        plt.draw()

        # p = plt.figure(figsize=(9, 7))

        p1 = plt.subplot(2, 1, 1)
        plt.title(f'Triple Screen Trading - First Screen ({code})')
        plt.grid(True)
        candlestick_ohlc(p1, ohlc.get_ohlc_data(), width=.1, colorup='red', colordown='blue')  # ⑦
        p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        for trading_point in macd.get_trading_points():
            plt.plot(trading_point.get("x"), trading_point.get("y"), trading_point.get("marker"))

        p2 = plt.subplot(2, 1, 2)
        plt.grid(True)
        p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        macd_histogram_data = macd.get_histogram_data()
        plt.bar(macd_histogram_data.get("x"), macd_histogram_data.get("y"), color='m', label='MACD-Hist')
        macd_data = macd.get_macd_data()
        plt.plot(macd_data.get("x"), macd_data.get("y"), color='b', label='MACD')
        macd_signal_data = macd.get_signal_data()
        plt.plot(macd_signal_data.get("x"), macd_signal_data.get("y"), 'g--', label='MACD-Signal')
        plt.legend(loc='best')

        plt.show()

    def append_text(self):
        text = self.le.text()
        self.tb.append(text)
        self.le.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
