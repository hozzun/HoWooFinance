from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# 사용자 모델 정의
class User(AbstractUser):
    userid = models.CharField(max_length=10, unique=True, null=True)
    username = models.CharField(max_length=10)
    age = models.IntegerField(default=20)
    gender = models.IntegerField(default=1)
    salary = models.IntegerField(default=-1)
    wealth = models.IntegerField(default=-1)
    period = models.IntegerField(default=-1)
    # deposit = models.ManyToManyField()
    # saving = models.ManyToManyField()
    
    USERNAME_FIELD = 'userid'
    
    def __str__(self):
        return self.userid or self.username