import json
from datetime import datetime, timedelta

from django_pandas.io import read_frame
from pandas import DataFrame

from mongoDBApp.models import MatchedRulesModel
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
        matched_rules_res = {}
        for i, company in enumerate(companies):
            code = company['code']
            print(code, i, start_date_text, end_date_text)
            daily_price_df = AnalysisService.get_daily_price(code, start_date_text, end_date_text)

            try:
                matched_rule = RuleExecutor().execute(daily_price_df)
                if matched_rule:
                    matched_rules_res[code] = matched_rule

                # matched_rules 저장
                analysis_date_text = daily_price_df.iloc[-1]['date']
                analysis_date = datetime.strptime(analysis_date_text, date_format).date()
                AnalysisService.save_analysis(code, analysis_date, matched_rule)
            except Exception as e:
                print(f"실패! {code}", e)

        return matched_rules_res

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

    @staticmethod
    def save_analysis(code, analysis_date, matched_rule):
        # TODO : 여러 rule 결과를 저장하도록 변경 필요 (현재는 단일 default rule 저장)
        rules = {
            'default': {
                'matched_rule': matched_rule
            }
        }
        your_model_instance = MatchedRulesModel(code=code,
                                                analysis_date=analysis_date,
                                                rules=rules)
        your_model_instance.save()
