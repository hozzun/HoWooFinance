from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


# 사용자 모델 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'name', 'age', 'gender', 'salary', 'wealth', 'period']


# 회원가입 시리얼라이저
class UserRegisterSerializer(RegisterSerializer):
    # 필드 확장
    name = serializers.CharField(required=False, allow_null=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    gender = serializers.IntegerField(required=False, allow_null=True)
    salary = serializers.IntegerField(required=False, allow_null=True)
    wealth = serializers.IntegerField(required=False, allow_null=True)
    period = serializers.IntegerField(required=False, allow_null=True)

    # 이메일 필드 제거
    email = None

    # 입력된 데이터 유효성 검사 후 가져오기
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'name': self.validated_data.get('name', None),
            'age': self.validated_data.get('age', None),
            'gender': self.validated_data.get('gender', None),
            'salary': self.validated_data.get('salary', None),
            'wealth': self.validated_data.get('wealth', None),
            'period': self.validated_data.get('period', None),
        })
        return data
    
    # 데이터 저장(사용자 등록)
    def save(self, request):
        user = super().save(request)
        user.name = self.validated_data.get('name')
        user.age = self.validated_data.get('age')
        user.gender = self.validated_data.get('gender')
        user.salary = self.validated_data.get('salary')
        user.wealth = self.validated_data.get('wealth')
        user.period = self.validated_data.get('period')
        user.save()
        return user


# 로그인 이메일 필드 제거
class UserLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=False, allow_null=True)
    email = None
    

# 사용자 세부정보(변경) 시리얼라이저
class UserDetailInfoSerializer(UserDetailsSerializer):
    # 필드 확장
    name = serializers.CharField(required=False, allow_null=True)
    age = serializers.CharField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_null=True)
    salary = serializers.CharField(required=False, allow_null=True)
    wealth = serializers.CharField(required=False, allow_null=True)
    period = serializers.CharField(required=False, allow_null=True)
    
    class Meta(UserDetailsSerializer.Meta):
        model = get_user_model()
        fields = ['name', 'age', 'gender', 'salary', 'wealth', 'period']

    # 입력된 데이터 유효성 검사 후 가져오기
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'name': self.validated_data.get('name', None),
            'age': self.validated_data.get('age', None),
            'gender': self.validated_data.get('gender', None),
            'salary': self.validated_data.get('salary', None),
            'wealth': self.validated_data.get('wealth', None),
            'period': self.validated_data.get('period', None),
        })
        return data
    
    # 기존 사용자 정보 업데이트
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.name = validated_data.get('name', None)
        instance.age = validated_data.get('age', None)
        instance.gender = validated_data.get('gender', None)
        instance.salary = validated_data.get('salary', None)
        instance.wealth = validated_data.get('wealth', None)
        instance.period = validated_data.get('period', None)
        instance.save()
        return instance