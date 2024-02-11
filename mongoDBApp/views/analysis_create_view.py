from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from mongoDBApp.models import MatchedRulesModel


class AnalysisCreateAPIView(APIView):
    def get(self, request):
        ordered_dict_data = {
            '1': {
                'matched_rule': False
            }, '2': {
                'matched_rule': False
            }
        }
        your_model_instance = MatchedRulesModel(code='101011',
                                                analysis_date=datetime.now().date(),
                                                rules=ordered_dict_data)
        your_model_instance.save()
        return Response({"ㅗ": "ㅁ"})
