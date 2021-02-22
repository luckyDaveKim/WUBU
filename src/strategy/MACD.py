import copy
import matplotlib.dates as mdates


class MACD:
    def __init__(self, df):
        self.__macd_df = self.__macd_dataframe(df)
        self.__trading_points = self.__calc_trading_points(self.__macd_df)
        self.__trading_points2 = self.__calc_trading_points2(self.__macd_df)

    def __macd_dataframe(self, df):
        ema60 = df.close.ewm(span=60).mean()  # ① 종가의 12주 지수 이동평균
        ema130 = df.close.ewm(span=130).mean()  # ② 종가의 12주 지수 이동평균
        macd = ema60 - ema130  # ③ MACD선
        signal = macd.ewm(span=45).mean()  # ④ 신호선(MACD의 9주 지수 이동평균)
        macdhist = macd - signal  # ⑤ MACD 히스토그램

        df = df.assign(ema60=ema60, ema130=ema130, macd=macd, signal=signal, macdhist=macdhist)
        df['number'] = df.index.map(mdates.date2num)  # ⑥
        return df

    def __calc_trading_points(self, df):
        trading_point = []
        for i in range(2, len(df)):
            oneBeforeGradient = df.macdhist.values[i - 1] - df.macdhist.values[i - 2]
            curGradient = df.macdhist.values[i] - df.macdhist.values[i - 1]
            isBuyTime = df.macdhist.values[i] < 0 and \
                        oneBeforeGradient <= 0 and \
                        curGradient >= 0
            isSellTime = df.macdhist.values[i] > 0 and \
                         oneBeforeGradient >= 0 and \
                         curGradient <= 0
            if isBuyTime:
                trading_point.append(
                    {"x": df.number.values[i], "y": df.close.values[i], "marker": "r^", "weight": 1, "trading": "buy"})
            if isSellTime:
                trading_point.append(
                    {"x": df.number.values[i], "y": df.close.values[i], "marker": "bv", "weight": 1, "trading": "sell"})
        return trading_point

    def __calc_trading_points2(self, df):
        trading_point = []
        for i in range(3, len(df)):
            twoBeforeGradient = df.macdhist.values[i - 2] - df.macdhist.values[i - 3]
            oneBeforeGradient = df.macdhist.values[i - 1] - df.macdhist.values[i - 2]
            curGradient = df.macdhist.values[i] - df.macdhist.values[i - 1]
            isBuyTime = df.macdhist.values[i] < 0 and \
                        twoBeforeGradient <= 0 and \
                        oneBeforeGradient >= 0 and \
                        curGradient >= 0
            isSellTime = df.macdhist.values[i] > 0 and \
                         twoBeforeGradient >= 0 and \
                         oneBeforeGradient <= 0 and \
                         curGradient <= 0
            if isBuyTime:
                trading_point.append(
                    {"x": df.number.values[i], "y": df.close.values[i], "marker": "r^", "weight": 1, "trading": "buy"})
            if isSellTime:
                trading_point.append(
                    {"x": df.number.values[i], "y": df.close.values[i], "marker": "bv", "weight": 1, "trading": "sell"})
        return trading_point

    def get_macd_data(self):
        return copy.deepcopy({"x": self.__macd_df.number, "y": self.__macd_df.macd})

    def get_signal_data(self):
        return copy.deepcopy({"x": self.__macd_df.number, "y": self.__macd_df.signal})

    def get_histogram_data(self):
        return copy.deepcopy({"x": self.__macd_df.number, "y": self.__macd_df.macdhist})

    def get_trading_points(self):
        return copy.deepcopy(self.__trading_points)

    def get_trading_points2(self):
        return copy.deepcopy(self.__trading_points2)
