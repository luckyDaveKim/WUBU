from wubuApp.models.dailyPriceStrategy.strategy_executable import StrategyExecutable


class BollingerBandExecutor(StrategyExecutable):
    def get_strategy_name(self):
        return 'bollingerBand'

    def execute(self, df):
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['bollingerBandStd'] = df['close'].rolling(window=20).std()
        df['bollingerBandUpper'] = df['ma20'] + (df['bollingerBandStd'] * 2)
        df['bollingerBandLower'] = df['ma20'] - (df['bollingerBandStd'] * 2)
        return df
