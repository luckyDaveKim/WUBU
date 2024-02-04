from datetime import datetime

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models.company_info_model import CompanyInfoModel
from .models.daily_price_model import DailyPriceModel
from .serializers.company_info_serializer import CompanyInfoSerializer
from .serializers.daily_price_serializer import DailyPriceSerializer


class CompaniesAPI(APIView):
    def get(self, request):
        market_type = 'KOSPI'
        queryset = CompanyInfoModel.objects.filter(market_type=market_type).order_by('company')
        serializer = CompanyInfoSerializer(queryset, many=True)
        return Response(serializer.data)


class DailyPriceAPI(APIView):
    def get(self, request, code):
        date_format = '%Y-%m-%d'

        start_date = request.GET.get('startDate', None)
        end_date = request.GET.get('endDate', None)

        filters = [('code', code)]
        try:
            if start_date and end_date:
                filters.append(
                    (
                        'date__range',
                        [datetime.strptime(start_date, date_format), datetime.strptime(end_date, date_format)]
                    )
                )
                filters.append(
                    (
                        'date__range',
                        [start_date, end_date]
                    )
                )
            elif start_date:
                filters.append(
                    ('date__gte', datetime.strptime(start_date, date_format))
                )
            elif end_date:
                filters.append(
                    ('date__lte', datetime.strptime(end_date, date_format))
                )
        except Exception as e:
            print('start_date, end_date 파싱 오류!!!', e)

        print('filter', *filters)
        queryset = DailyPriceModel.objects.filter(*filters).order_by('date')
        serializer = DailyPriceSerializer(queryset, many=True)
        return Response(serializer.data)


def product_list(request):
    company_infos = CompanyInfoModel.objects.all()
    return render(request, 'company/company_list.html', {'company_infos': company_infos})


def product_detail(request, pk):
    print(pk)
    company_info = CompanyInfoModel.objects.get(pk=pk)
    return render(request, 'company/company_detail.html', {'company_info': company_info})
