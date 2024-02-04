import pandas as pd

from wubuApp.models.dailyPriceStrategy.strategy_executable import StrategyExecutable


class CandleChartDataExecutor(StrategyExecutable):
    def get_strategy_name(self):
        return 'dailyPrice'

    def execute(self, df):
        df['price'] = df.apply(lambda row: [row['open'], row['high'], row['low'], row['close']], axis=1)
        df['date_timestamp'] = pd.to_datetime(df['date']).astype(int) / 10 ** 9

        return df
