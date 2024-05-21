from django.db import models
from django.conf import settings

# Create your models here.

# 적금 상품정보 모델
class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품 코드
    fin_prdt_nm = models.TextField()             # 금융 상품명
    kor_co_nm = models.TextField()               # 금융회사 명
    mtrt_int = models.TextField()                # 만기 후 이자율
    spcl_cnd = models.TextField()                # 우대조건
    join_way = models.TextField()                # 가입 방법
    join_deny = models.TextField()               # 가입제한
    join_member = models.TextField()             # 가입대상
    etc_note = models.TextField()                # 기타 유의사항


# 적금 옵션정보 모델
class SavingOptions(models.Model):
    fin_prdt_cd = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)
    intr_rate_type_nm = models.CharField(max_length=100)                # 저축 금리 유형명
    save_trm = models.IntegerField(default=0)                           # 저축 기간
    intr_rate = models.FloatField(default=0, null=True, blank=True)     # 저축 금리
    intr_rate2 = models.FloatField(default=0, null=True, blank=True)    # 최고 우대금리   
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_saving_options', blank=True)

    class Meta:
        unique_together = ('fin_prdt_cd', 'save_trm')