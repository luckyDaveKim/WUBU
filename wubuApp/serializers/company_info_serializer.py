from rest_framework import serializers

from wubuApp.models import CompanyInfoModel


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfoModel
        fields = '__all__'
