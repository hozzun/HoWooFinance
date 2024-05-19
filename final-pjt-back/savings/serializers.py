from rest_framework import serializers
from .models import SavingProducts, SavingOptions


# 적금 옵션목록 시리얼라이저
class SavingOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd', )


# 적금 상품목록 시리얼라이저
class SavingProductsSerializer(serializers.ModelSerializer):
    saving_options = SavingOptionsSerializer(many=True, read_only=True, source='savingoptions_set')
    
    class Meta:
        model = SavingProducts
        fields = '__all__'