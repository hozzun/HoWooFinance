from django.db import models
from django.conf import settings  # settings 모듈을 가져옵니다.

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # auth.User 대신 settings.AUTH_USER_MODEL을 사용합니다.
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatHistory(user={self.user}, timestamp={self.timestamp})"
