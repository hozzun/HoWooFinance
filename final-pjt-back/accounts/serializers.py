from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


# 로그인 화면 이메일 필드 제거
class UserLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=False, allow_null=True)
    email = None

# 사용자 모델 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'age', 'gender', 'salary', 'wealth', 'period']

# 회원가입 시리얼라이저
class UserRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=False, allow_null=True)
    gender = serializers.IntegerField(required=False, allow_null=True)
    salary = serializers.IntegerField(required=False, allow_null=True)
    wealth = serializers.IntegerField(required=False, allow_null=True)
    period = serializers.IntegerField(required=False, allow_null=True)

    # 이메일 필드 제거
    email = None

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'age': self.validated_data.get('age', None),
            'gender': self.validated_data.get('gender', None),
            'salary': self.validated_data.get('salary', None),
            'wealth': self.validated_data.get('wealth', None),
            'period': self.validated_data.get('period', None),
        })
        return data
    
    def save(self, request):
        user = super().save(request)
        user.age = self.validated_data.get('age')
        user.gender = self.validated_data.get('gender')
        user.salary = self.validated_data.get('salary')
        user.wealth = self.validated_data.get('wealth')
        user.period = self.validated_data.get('period')
        user.save()
        return user