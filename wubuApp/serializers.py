from rest_framework import serializers
from .models import CompanyInfo


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = '__all__'
