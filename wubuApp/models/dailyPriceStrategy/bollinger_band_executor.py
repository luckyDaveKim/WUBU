from wubuApp.models.dailyPriceStrategy.strategy_executable import StrategyExecutable


class BollingerBandExecutor(StrategyExecutable):
    def get_strategy_name(self):
        return 'bollingerBand'

    def execute(self, df):
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['bollingerBandStdDev'] = df['close'].rolling(window=20).std()
        df['bollingerBandUpper'] = df['ma20'] + (df['bollingerBandStdDev'] * 2)
        df['bollingerBandLower'] = df['ma20'] - (df['bollingerBandStdDev'] * 2)

        # 미사용 필드 제거
        df.drop('bollingerBandStdDev', axis=1)

        return df
