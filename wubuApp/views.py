from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CompanyInfo
from .serializers import CompaniesSerializer

class CompaniesAPI(APIView):
    def get(self, request):
        queryset = CompanyInfo.objects.all()
        print(queryset)
        serializer = CompaniesSerializer(queryset, many=True)
        return Response(serializer.data)


def product_list(request):
    company_infos = CompanyInfo.objects.all()
    return render(request, 'company/company_list.html', {'company_infos': company_infos})


def product_detail(request, pk):
    print(pk)
    company_info = CompanyInfo.objects.get(pk=pk)
    return render(request, 'company/company_detail.html', {'company_info': company_info})
