from rest_framework.response import Response
from rest_framework.views import APIView

from wubuApp.models import CompanyInfoModel, CompanyInfoFilterCondition
from wubuApp.serializers import CompanyInfoSerializer


class CompaniesAPIView(APIView):
    def get(self, request):
        condition = CompanyInfoFilterCondition.builder().set_market_type('KOSPI').build()

        queryset = CompanyInfoModel.objects.filter(*condition.get_filter()).order_by('company')
        serializer = CompanyInfoSerializer(queryset, many=True)
        return Response(serializer.data)
