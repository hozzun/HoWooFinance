from django.db import models

# Create your models here.

# 금융상품 기본정보 모델
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품 코드
    fin_prdt_nm = models.TextField()             # 금융 상품명
    kor_co_nm = models.TextField()               # 금융회사 명
    mtrt_int = models.TextField()                # 만기 후 이자율
    spcl_cnd = models.TextField()                # 우대조건
    join_way = models.TextField()                # 가입 방법
    join_deny = models.TextField()               # 가입제한
    join_member = models.TextField()             # 가입대상
    etc_note = models.TextField()                # 기타 유의사항


# 금융상품 옵션목록 모델
class DepositOptions(models.Model):
    fin_prdt_cd = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    intr_rate_type_nm = models.CharField(max_length=100)     # 저축 금리 유형명
    save_trm = models.IntegerField(default=0)                # 저축 기간
    intr_rate = models.FloatField(default=0)                 # 저축 금리
    intr_rate2 = models.FloatField(default=0)                # 최고 우대금리   