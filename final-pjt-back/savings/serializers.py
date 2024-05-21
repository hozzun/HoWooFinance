from rest_framework import serializers
from .models import SavingProducts, SavingOptions


# 적금 옵션목록 시리얼라이저
class SavingOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd', )

    # 값 없을 경우 대비
    def validate_intr_rate2(self, value):
        if value is None:
            return 0.0
        return value


# 적금 상품목록 시리얼라이저
class SavingProductsSerializer(serializers.ModelSerializer):
    saving_options = SavingOptionsSerializer(many=True, read_only=True, source='savingoptions_set')
    
    class Meta:
        model = SavingProducts
        fields = '__all__'
    
    # 해당 적금 상품 옵션 같이 묶기
    def get_saving_options(self, obj):
        request = self.context.get('request')
        user = request.user
        return SavingOptionsSerializer(obj.savingoptions_set.filter(users=user), many=True).data