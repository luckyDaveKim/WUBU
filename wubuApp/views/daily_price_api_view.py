import json

from rest_framework.response import Response
from rest_framework.views import APIView

from wubuApp.models import DailyPriceModel, DailyPriceFilterCondition
from wubuApp.models.dailyPriceStrategy import StrategyExecutorFactory


class DailyPriceAPIView(APIView):
    def get(self, request, code):
        condition = (DailyPriceFilterCondition
                     .builder()
                     .set_code(code)
                     .set_start_date(request.GET.get('startDate', None))
                     .set_end_date(request.GET.get('endDate', None))
                     .build())

        queryset = DailyPriceModel.objects.filter(*condition.get_filter()).order_by('date')

        df = StrategyExecutorFactory(queryset).execute_all(request.GET.get('strategyNames', []))
        json_data = json.loads(df.to_json(orient='records'))

        return Response(json_data)
