from django.db import models
from django.contrib.auth.models import AbstractUser
from deposits.models import DepositProducts, DepositOptions
from savings.models import SavingProducts, SavingOptions

# Create your models here.

# 사용자 모델 정의
class User(AbstractUser):
    # 이메일
    username = models.CharField(max_length=30, unique=True)
    # 이름
    name = models.CharField(max_length=10, default='unKnown')
    # 나이
    age = models.IntegerField(default=20)
    # 성별
    gender = models.IntegerField(default=1)
    # 연봉
    salary = models.IntegerField(default=0)
    # 희망 금액
    wealth = models.IntegerField(default=0)
    # 희망 기간
    period = models.IntegerField(default=0)
    # 정기예금 상품
    deposit = models.ManyToManyField(DepositProducts, blank=True, related_name='deposit_joined')
    # 적금 상품
    saving = models.ManyToManyField(SavingProducts, blank=True, related_name='saving_joined')
    # 정기예금 옵션
    deposit_options = models.ManyToManyField(DepositOptions, blank=True, related_name='user_deposit_options')
    # 적금 옵션
    saving_options = models.ManyToManyField(SavingOptions, blank=True, related_name='users_saving_options')