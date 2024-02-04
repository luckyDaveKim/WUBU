from rest_framework.response import Response
from rest_framework.views import APIView

from wubuApp.models import CompanyInfoModel
from wubuApp.serializers import CompanyInfoSerializer


class CompaniesAPI(APIView):
    def get(self, request):
        market_type = 'KOSPI'
        queryset = CompanyInfoModel.objects.filter(market_type=market_type).order_by('company')
        serializer = CompanyInfoSerializer(queryset, many=True)
        return Response(serializer.data)
