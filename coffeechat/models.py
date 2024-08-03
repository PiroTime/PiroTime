from django.db import models
from accounts.models import CustomUser
# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name  # 해시태그의 이름을 반환

class CoffeeChat(models.Model):
    STATUS_CHOICES = [
        ('WAITING','수락대기중'),
        ('COMPLETED','수락'),
        ('LIMITED','최대요청횟수초과'),
        ('Private','비공개')
    ]
    username = models.ForeignKey(CustomUser, related_name='sent_coffeechats', on_delete=models.CASCADE, null=True, blank=True) #커피챗 요청자
    receiver = models.ForeignKey(CustomUser, related_name='received_coffeechats', on_delete=models.CASCADE) #커피챗 요청받은 사람
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='WAITING') #커피챗 상태
    job = models.CharField(max_length=10, null=False) #직업
    created_at = models.DateTimeField(auto_now_add=True) #요청시간
    hashtags = models.ManyToManyField(Hashtag, related_name='coffeechats') #해시태그
    content = models.TextField(null=True, blank=True) #자기소개
    count = models.IntegerField(default=0) #요청 수
    