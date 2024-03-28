import json
from datetime import datetime

from django_pandas.io import read_frame
from rest_framework.response import Response
from rest_framework.views import APIView

from mongoDBApp.models import MatchedRulesModel, MatchedRulesFilterCondition
from wubuApp.services.analysis_service import AnalysisService


class AnalysisAPIView(APIView):
    def get(self, request):
        condition = (MatchedRulesFilterCondition
                     .builder()
                     .set_code(request.GET.get('code', None))
                     .set_analysis_date(request.GET.get('analysisDate', None))
                     .set_start_analysis_date(request.GET.get('startAnalysisDate', None))
                     .set_end_analysis_date(request.GET.get('endAnalysisDate', None))
                     .build())


        # e = MatchedRulesModel()
        # e.code = '131313'
        # e.rules = 'good'
        # e.save()

        MatchedRulesModel(code='121211', rules='hoho3323').save()
        # MatchedRulesModel.objects.create(code='121212', rules='hoho4')

        # model = MatchedRulesModel(code='123121', rules='123123')
        # model.save()
        # MatchedRulesModel.objects.create(code='121213', rules='hoho')
        # MatchedRulesModel(code='123121', analysis_date=datetime.now(), rules="{'myrule': {'a': 'b'}}").save()
        queryset = MatchedRulesModel.objects.filter(*condition.get_filter())
        # queryset = MatchedRulesModel.objects.filter(*condition.get_filter()).order_by('code', '-analysis_date')
        # queryset = MatchedRulesModel.objects()
        # df = read_frame(queryset)
        # json_data = json.loads(df.to_json(orient='records'))
        # return Response(json_data)
        for person in queryset:
            print(person.code)

        return Response(True)

    def post(self, request):
        target_date_text = request.GET.get('targetDate', datetime.now().strftime("%Y-%m-%d"))
        res = AnalysisService.analysis(target_date_text)

        return Response(res)
