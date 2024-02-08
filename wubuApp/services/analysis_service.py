import json
from datetime import datetime, timedelta

from django_pandas.io import read_frame
from pandas import DataFrame

from wubuApp.models import DailyPriceFilterCondition, DailyPriceModel, CompanyInfoFilterCondition, CompanyInfoModel
from wubuApp.models.dailyPriceStrategy import StrategyExecutorFactory
from wubuApp.models.ruleStrategy.rule_executor import RuleExecutor


class AnalysisService:
    @staticmethod
    def analysis(target_date_text):
        duration_days = 45
        date_format = "%Y-%m-%d"
        target_date = datetime.strptime(target_date_text, date_format)
        start_date_text = (target_date - timedelta(days=duration_days)).strftime(date_format)
        end_date_text = target_date.strftime(date_format)

        companies = AnalysisService.get_all_companies()
        res = {}
        for i, company in enumerate(companies):
            code = company['code']
            print(code, i, start_date_text, end_date_text)
            daily_price_df = AnalysisService.get_daily_price(code, start_date_text, end_date_text)
            try:
                matched_rule = RuleExecutor().execute(daily_price_df)
                if matched_rule:
                    res[code] = matched_rule
            except Exception as e:
                print(f"실패! {code}", e)

        return res

    @staticmethod
    def get_all_companies():
        condition = CompanyInfoFilterCondition.builder().set_market_type('KOSPI').build()

        queryset = CompanyInfoModel.objects.filter(*condition.get_filter()).order_by('company')
        df = read_frame(queryset)
        json_text = df.to_json(orient='records')
        return json.loads(json_text)

    @staticmethod
    def get_daily_price(code, start_date_text, end_date_text) -> DataFrame:
        condition = (DailyPriceFilterCondition
                     .builder()
                     .set_code(code)
                     .set_start_date(start_date_text)
                     .set_end_date(end_date_text)
                     .build())

        queryset = DailyPriceModel.objects.filter(*condition.get_filter()).order_by('date')
        df = StrategyExecutorFactory(queryset).execute_all(['bollingerBand'])
        return df
