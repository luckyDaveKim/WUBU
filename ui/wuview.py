import sys
import threading
from datetime import datetime
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure
import numpy as np
import matplotlib.dates as mdates

import matplotlib
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from data import MarketDB
from strategy.MACD import MACD
from strategy.OHLC import OHLC
from strategy.BollingerBand import BollingerBand


class MainWindow(QMainWindow):
    scanRunning = False
    mk = MarketDB.MarketDB()

    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle('Dave')
        self.setGeometry(600, 200, 1200, 800)

        self.statusBar().showMessage('Ready')

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.visualization = WidgetPlot(self)

        self.scanBtn = QPushButton('스캔', self)
        self.scanBtn.clicked.connect(self.onScanBtnClick)

        self.stopBtn = QPushButton('정지', self)
        self.stopBtn.clicked.connect(self.onStopBtnClick)

        self.stockComboBox = QComboBox(self)
        self.stockComboBox.activated[str].connect(self.onStockComboBoxActivated)

        self.preBtn = QPushButton('이전', self)
        self.preBtn.clicked.connect(self.onPreBtnClick)

        self.nextBtn = QPushButton('다음', self)
        self.nextBtn.clicked.connect(self.onNextBtnClick)

        self.startDateEdit = QDateEdit(self)
        self.startDateEdit.setDate(QDate.currentDate().addYears(-2))

        self.endDateEdit = QDateEdit(self)
        self.endDateEdit.setDate(QDate.currentDate())

        self.stockLineEdit = QLineEdit(self)

        self.drawBtn = QPushButton('차트 그리기', self)
        self.drawBtn.clicked.connect(self.onDrawBtnClick)

        self.initLayout()

    def initLayout(self):
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.visualization)

        scanBtnLayout = QHBoxLayout()
        scanBtnLayout.addWidget(self.scanBtn)
        scanBtnLayout.addWidget(self.stopBtn)

        pagingBtnLayout = QHBoxLayout()
        pagingBtnLayout.addWidget(self.preBtn)
        pagingBtnLayout.addWidget(self.nextBtn)

        dateLayout = QHBoxLayout()
        dateLayout.addWidget(self.startDateEdit)
        dateLayout.addWidget(self.endDateEdit)

        rightLayout = QVBoxLayout()
        rightLayout.addLayout(scanBtnLayout)
        rightLayout.addWidget(self.stockComboBox)
        rightLayout.addLayout(pagingBtnLayout)
        rightLayout.addLayout(dateLayout)
        rightLayout.addWidget(self.stockLineEdit)
        rightLayout.addWidget(self.drawBtn)
        rightLayout.addStretch(1)

        layout = QHBoxLayout(self.widget)
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)

    def onScanBtnClick(self):
        self.statusBar().showMessage("스캔 시작")
        self.stockComboBox.clear()
        threading.Thread(target=self.scan, args=(self.startDateEdit.text(), self.endDateEdit.text())).start()

    def scan(self, start_date, end_date):
        mk = MarketDB.MarketDB()
        self.scanRunning = True
        codes = mk.get_codes().values()
        for i, code in enumerate(codes):
            self.statusBar().showMessage(f"[{start_date} ~ {end_date}] 스캔중... ({i + 1} / {len(codes) + 1})")
            if not self.scanRunning:
                self.statusBar().showMessage(f"[{start_date} ~ {end_date}] 스캔 종료 ({i + 1} / {len(codes) + 1})")
                break

            df = mk.get_daily_price(code, start_date, end_date)
            today_x_value = mdates.date2num(np.datetime64(datetime.today().strftime('%Y-%m-%d')))

            bollinger_band = BollingerBand(df)
            bollinger_band_trading_points = bollinger_band.get_trading_points()
            if len(bollinger_band_trading_points) == 0:
                continue
            bollinger_band_trading_point = bollinger_band_trading_points[-1]

            macd = MACD(df)
            macd_trading_points = macd.get_trading_points()
            if len(macd_trading_points) == 0:
                continue
            macd_trading_point = macd_trading_points[-1]

            if bollinger_band_trading_point.get("x") == today_x_value and \
                    bollinger_band_trading_point.get("trading") == "buy" and \
                    macd_trading_point.get("x") == today_x_value and \
                    macd_trading_point.get("trading") == "buy":
                if bollinger_band_trading_point.get("weight") + macd_trading_point.get("weight") >= 1:
                    self.stockComboBox.addItem(code)
        if self.scanRunning:
            self.statusBar().showMessage(f"[{start_date} ~ {end_date}] 스캔 완료")
            self.scanRunning = False

    def onStopBtnClick(self):
        self.scanRunning = False

    def onStockComboBoxActivated(self, code):
        self.stockLineEdit.clear()
        self.stockLineEdit.setText(code)

    def onPreBtnClick(self):
        text = self.stockComboBox.currentText()
        index = self.stockComboBox.findText(text)
        if index > 0:
            self.stockComboBox.setCurrentIndex(index - 1)
            text = self.stockComboBox.currentText()
            self.onStockComboBoxActivated(text)
            self.onDrawBtnClick()

    def onNextBtnClick(self):
        text = self.stockComboBox.currentText()
        index = self.stockComboBox.findText(text)
        if index < self.stockComboBox.count() - 1:
            self.stockComboBox.setCurrentIndex(index + 1)
            text = self.stockComboBox.currentText()
            self.onStockComboBoxActivated(text)
            self.onDrawBtnClick()

    def onDrawBtnClick(self):
        code = self.stockLineEdit.text()
        df = self.mk.get_daily_price(code, self.startDateEdit.text(), self.endDateEdit.text())
        self.visualization.changeData(code, df)


class WidgetPlot(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)

    def changeData(self, code, df):
        self.canvas.changeData(code, df)
        self.toolbar.update()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        matplotlib.rcParams['font.family'] = "Malgun Gothic"
        matplotlib.rcParams['axes.unicode_minus'] = False
        fig = Figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        self.candle_chart = self.figure.add_subplot(3, 1, 1)
        self.bollinger_band_chart = self.figure.add_subplot(3, 1, 2, sharex=self.candle_chart)
        self.macd_chart = self.figure.add_subplot(3, 1, 3, sharex=self.candle_chart)

    def changeData(self, code, df):
        ohlc = OHLC(df)
        bollinger_band = BollingerBand(df)
        macd = MACD(df)

        self.candle_chart.clear()
        self.candle_chart.set_title(code)
        candlestick_ohlc(self.candle_chart, ohlc.get_ohlc_data(), width=.1, colorup='red', colordown='blue')
        for trading_point in macd.get_trading_points():
            self.candle_chart.plot(trading_point.get("x"), trading_point.get("y"), trading_point.get("marker"))
        self.candle_chart.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
        self.candle_chart.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
        self.candle_chart.grid(True)

        self.bollinger_band_chart.clear()
        bollinger_band_close_data = bollinger_band.get_close_data()
        self.bollinger_band_chart.plot(bollinger_band_close_data.get("x"), bollinger_band_close_data.get("y"),
                                       color='m', label='Close')
        bollinger_band_upper_band_data = bollinger_band.get_upper_band_data()
        self.bollinger_band_chart.plot(bollinger_band_upper_band_data.get("x"), bollinger_band_upper_band_data.get("y"),
                                       'r--', label='Upper band')
        bollinger_band_ma20_data = bollinger_band.get_ma20_band_data()
        self.bollinger_band_chart.plot(bollinger_band_ma20_data.get("x"), bollinger_band_ma20_data.get("y"), 'k--',
                                       label='Moving average 20')
        bollinger_band_lower_band_data = bollinger_band.get_lower_band_data()
        self.bollinger_band_chart.plot(bollinger_band_lower_band_data.get("x"), bollinger_band_lower_band_data.get("y"),
                                       'c--', label='Lower band')
        self.bollinger_band_chart.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
        self.bollinger_band_chart.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
        self.bollinger_band_chart.grid(True)
        self.bollinger_band_chart.legend(loc='best')

        self.macd_chart.clear()
        macd_data = macd.get_macd_data()
        self.macd_chart.plot(macd_data.get("x"), macd_data.get("y"), color='b', label='MACD')
        macd_signal_data = macd.get_signal_data()
        self.macd_chart.plot(macd_signal_data.get("x"), macd_signal_data.get("y"), 'g--', label='MACD-Signal')
        macd_histogram_data = macd.get_histogram_data()
        self.macd_chart.bar(macd_histogram_data.get("x"), macd_histogram_data.get("y"), color='m', label='MACD-Hist')
        self.macd_chart.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
        self.macd_chart.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
        self.macd_chart.grid(True)
        self.macd_chart.legend(loc='best')

        self.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
