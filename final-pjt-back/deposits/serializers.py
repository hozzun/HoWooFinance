from rest_framework import serializers
from .models import DepositProducts, DepositOptions


# 금융 옵션목록 시리얼라이저
class DepositOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        models = DepositOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd', )


# 금융 상품목록 시리얼라이저
class DepositProductsSerializer(serializers.ModelSerializer):
    option_set = DepositOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProducts
        fields = '__all__'

