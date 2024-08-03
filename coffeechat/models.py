from django.db import models
from accounts.models import CustomUser
# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

class CoffeeChat(models.Model):
    STATUS_CHOICES = [
        ('WAITING','수락대기중'),
        ('COMPLETED','수락'),
        ('LIMITED','최대요청횟수초과'),
        ('Private','비공개')
    ]
    username = models.ForeignKey(CustomUser, related_name='username', on_delete=models.CASCADE) #커피챗 요청자
    receiver = models.ForeignKey(CustomUser, related_name='receiver', on_delete=models.CASCADE) #커피챗 요청받은 사람
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, defalut='WAITING') #커피챗 상태
    job = models.CharField(max_length=10, null=False) #직업
    created_at = models.DateTimeField(auto_now_add=True) #요청시간
    hashtags = models.ManyToManyField(Hashtag, related_name='coffeechats') #해시태그
    content = models.TextField(null=True, blank=True) #자기소개
    count = models.IntegerField() #요청 수


class AskCoffeeChat(models.Model):
    STATUS_ASK = [
        ('stay', '대기 중'),
        ('accepted', '수락'),
        ('rejected', '거절'),
        ('end', '종료')           #요청이 받아들여져 커피챗이 완료된 경우
    ]

    username = models.ForeignKey(CustomUser, related_name='username', on_delete=models.CASCADE) #커피챗 요청자
    receiver = models.ForeignKey(CustomUser, related_name='receiver', on_delete=models.CASCADE) #커피챗 요청받은 사람
    created_at = models.DateTimeField(auto_now_add=True) #요청시간
    post = models.ForeignKey(CoffeeChat, related_name="coffeechat", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_ASK, defalut='stay')