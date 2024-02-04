from django_pandas.io import read_frame

from wubuApp.models.dailyPriceStrategy.bollinger_band_executor import BollingerBandExecutor
from wubuApp.models.dailyPriceStrategy.cleanup_executor import CleanupExecutor
from wubuApp.models.dailyPriceStrategy.candle_chart_data_executor import CandleChartDataExecutor


class StrategyExecutorFactory:
    # 순서 중요
    _executors = [
        # pre executors...
        CandleChartDataExecutor(),

        # other executors...
        BollingerBandExecutor(),

        # post executors...
        CleanupExecutor(),
    ]

    _default_run_strategy_names = ['dailyPrice', 'cleanup']

    def __init__(self, queryset):
        self.df = read_frame(queryset)

    def execute_all(self, strategy_names):
        if not strategy_names:
            strategy_names = []

        if not isinstance(strategy_names, list):
            strategy_names = [strategy_names]

        strategy_names = strategy_names + self._default_run_strategy_names

        for executor in self._executors:
            if executor.get_strategy_name() not in strategy_names:
                continue

            self.df = executor.execute(self.df)

        return self.df
