from rest_framework import serializers
from wubuApp.models.company_info_model import CompanyInfoModel


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfoModel
        fields = '__all__'
