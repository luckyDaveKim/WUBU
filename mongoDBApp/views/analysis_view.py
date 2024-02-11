import json

from django_pandas.io import read_frame
from rest_framework.response import Response
from rest_framework.views import APIView

from mongoDBApp.models import MatchedRulesModel


class AnalysisAPIView(APIView):
    def get(self, request):
        # queryset = MatchedRulesModel.objects.all()
        # filters = [["code", "035420"]]
        # filters = [["rules", {"1": {"matched_rule": True}}]]
        queryset = MatchedRulesModel.objects.all()
        # queryset = MatchedRulesModel.objects.filter(*filters)
        df = read_frame(queryset)
        json_data = json.loads(df.to_json(orient='records'))

        return Response(json_data)
