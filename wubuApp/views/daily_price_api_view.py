from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from wubuApp.models import CompanyInfoModel, DailyPriceModel, DailyPriceFilterCondition
from wubuApp.serializers import DailyPriceSerializer


class DailyPriceAPIView(APIView):
    def get(self, request, code):
        condition = (DailyPriceFilterCondition()
                     .builder()
                     .set_code(code)
                     .set_start_date(request.GET.get('startDate', None))
                     .set_end_date(request.GET.get('endDate', None))
                     .build())

        queryset = DailyPriceModel.objects.filter(*condition.get_filter()).order_by('date')

        serializer = DailyPriceSerializer(queryset, many=True)
        return Response(serializer.data)


def product_list(request):
    company_infos = CompanyInfoModel.objects.all()
    return render(request, 'company/company_list.html', {'company_infos': company_infos})


def product_detail(request, pk):
    print(pk)
    company_info = CompanyInfoModel.objects.get(pk=pk)
    return render(request, 'company/company_detail.html', {'company_info': company_info})
