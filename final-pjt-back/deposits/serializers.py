from rest_framework import serializers
from .models import DepositProducts, DepositOptions


# 정기예금 옵션목록 시리얼라이저
class DepositOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd', )


# 정기예금 상품목록 시리얼라이저
class DepositProductsSerializer(serializers.ModelSerializer):
    deposit_options = DepositOptionsSerializer(many=True, read_only=True, source='depositoptions_set')
    
    class Meta:
        model = DepositProducts
        fields = '__all__'

    # 해당 유저가 가입한 정기예금 상품과 옵션 같이 묶기
    def get_deposit_options(self, obj):
        request = self.context.get('request')
        user = request.user
        return DepositOptionsSerializer(obj.depositoptions_set.filter(users=user), many=True).data