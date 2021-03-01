import copy
import matplotlib.dates as mdates


class OHLC:
    def __init__(self, df):
        self.__ohlc_df = self.__ohlc_dataframe(df)

    def __ohlc_dataframe(self, df):
        df['number'] = df.index.map(mdates.date2num)
        return df[['number', 'open', 'high', 'low', 'close']]

    def get_ohlc_data(self):
        return copy.deepcopy(self.__ohlc_df.values)
