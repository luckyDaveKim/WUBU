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
                     .set_analysis_date(request.GET.get('targetDate', datetime.now().strftime("%Y-%m-%d")))
                     .build())

        queryset = MatchedRulesModel.objects.filter(*condition.get_filter()).order_by('code')
        df = read_frame(queryset)
        json_data = json.loads(df.to_json(orient='records'))

        return Response(json_data)

    def post(self, request):
        target_date_text = request.GET.get('targetDate', datetime.now().strftime("%Y-%m-%d"))
        res = AnalysisService.analysis(target_date_text)

        return Response(res)
