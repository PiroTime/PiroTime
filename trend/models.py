from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Trend(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    refer_url = models.URLField(max_length=200, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='trend_likes', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='trend_bookmarks', blank=True)

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    trend = models.ForeignKey(Trend, related_name='comments', on_delete=models.CASCADE)
    
    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='trend_comments')
    
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.writer} on {self.trend}'