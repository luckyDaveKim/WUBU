from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from wubuApp.services.analysis_service import AnalysisService


class AnalysisAPIView(APIView):
    def get(self, request):
        target_date_text = request.GET.get('targetDate', datetime.now().strftime("%Y-%m-%d"))
        res = AnalysisService.analysis(target_date_text)

        return Response(res)
