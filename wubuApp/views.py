from django.shortcuts import render
from .models import CompanyInfo


def product_list(request):
    company_infos = CompanyInfo.objects.all()
    return render(request, 'company/company_list.html', {'company_infos': company_infos})


def product_detail(request, pk):
    print(pk)
    company_info = CompanyInfo.objects.get(pk=pk)
    return render(request, 'company/company_detail.html', {'company_info': company_info})
