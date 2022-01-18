import copy
import matplotlib.dates as mdates
from itertools import islice


class BollingerBand:
    def __init__(self, df):
        self.__bollinger_band_df = self.__bollinger_band_dataframe(df)
        self.__trading_points = self.__calc_trading_points(self.__bollinger_band_df)

    def __bollinger_band_dataframe(self, df):
        df['ma20'] = df.close.rolling(window=20).mean()  # 20개 종가를 이용한 평균
        df['stddev'] = df.close.rolling(window=20).std()  # 20개 종가를 이용한 표준편차
        df['upper'] = df.ma20 + (2 * df.stddev)  # 상단 볼린저 밴드
        df['lower'] = df.ma20 - (2 * df.stddev)  # 하단 볼린저 밴드
        df['PB'] = (df.close - df.lower) / (df.upper - df.lower)  # %B

        df['II'] = (2 * df.close - df.high - df.low) / (df.high - df.low) * df.volume  # 일중 강도
        df['IIP21'] = df.II.rolling(window=21).sum() / df.volume.rolling(window=21).sum() * 100  # 21일간 일중 강도
        df['number'] = df.index.map(mdates.date2num)  # ⑥

        return df

    def __calc_trading_points(self, df):
        trading_point = []
        for i in range(2, len(df)):
            before_pb = df.PB.values[i - 1]
            cur_pb = df.PB.values[i]
            gradient = cur_pb - before_pb
            increase = 0 < gradient
            decrease = gradient <= 0

            over_pb = 1 <= cur_pb
            high_pb = 0.85 <= cur_pb <= 1
            mid_high_pb = 0.5 < cur_pb <= 0.55
            mid_low_pb = 0.45 <= cur_pb < 0.5
            low_pb = 0 < cur_pb <= 0.15
            under_pb = cur_pb <= 0

            if over_pb and decrease:  # %b가 1이상이면, 최대한 먹고 하락할 때 판다
                trading_point.append(
                    {"x": df.number.values[i], "y": df.close.values[i], "marker": "bv", "weight": 1, "trading": "sell"})
            elif high_pb and decrease:  # %b가 높으면, 판다
                trading_point.append(
                    {"x": df.number.values[i], "y": df.close.values[i], "marker": "bv", "weight": cur_pb,
                     "trading": "sell"})
            elif mid_high_pb and decrease:  # %b가 좀 떨어지면 산다
                trading_point.append(
                    {"x": df.number.values[i], "y": df.close.values[i], "marker": "bv", "weight": cur_pb,
                     "trading": "buy"})
            elif mid_low_pb and increase:  # %b가 좀 오르면 판다
                trading_point.append(
                    {"x": df.number.values[i], "y": df.close.values[i], "marker": "bv", "weight": 1 - cur_pb,
                     "trading": "sell"})
            elif low_pb and increase:  # %b가 낮으면, 산다
                trading_point.append(
                    {"x": df.number.values[i], "y": df.close.values[i], "marker": "bv", "weight": 1 - cur_pb,
                     "trading": "buy"})
            elif under_pb and increase:  # %b가 1이상이면, 최대한 기다렸다가 상승할 때 산다
                trading_point.append(
                    {"x": df.number.values[i], "y": df.close.values[i], "marker": "bv", "weight": 1,
                     "trading": "buy"})
        return trading_point

    def get_close_data(self):
        return copy.deepcopy({"x": self.__bollinger_band_df.number, "y": self.__bollinger_band_df.close})

    def get_lower_band_data(self):
        return copy.deepcopy({"x": self.__bollinger_band_df.number, "y": self.__bollinger_band_df.lower})

    def get_ma20_band_data(self):
        return copy.deepcopy({"x": self.__bollinger_band_df.number, "y": self.__bollinger_band_df.ma20})

    def get_upper_band_data(self):
        return copy.deepcopy({"x": self.__bollinger_band_df.number, "y": self.__bollinger_band_df.upper})

    def get_pb_data(self):
        return copy.deepcopy({"x": self.__bollinger_band_df.number, "y": self.__bollinger_band_df.PB})

    def get_iip21_data(self):
        return copy.deepcopy({"x": self.__bollinger_band_df.number, "y": self.__bollinger_band_df.IIP21})

    def get_trading_points(self):
        return copy.deepcopy(self.__trading_points)
