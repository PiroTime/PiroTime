from django.db import models
from django.conf import settings
from django.urls import reverse

# 트렌드 모델
class Trend(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    refer_url = models.URLField(max_length=200, blank=True, null=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='trend_likes', 
        blank=True
    )
    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='trend_bookmarks', 
        blank=True
    )

    def total_likes(self):
        return self.likes.count()
    def total_bookmark(self):
        return self.bookmarks.count()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('trend:trend_detail', args=[self.id])
    
    def get_post_type(self):
        return 'trend'

# 트렌드에 대한 댓글 모델
class Comment(models.Model):
    trend = models.ForeignKey(
        Trend, 
        related_name='comments', 
        on_delete=models.CASCADE
    )
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='trend_comments'
    )
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='trend_replies', on_delete=models.CASCADE)

    def get_replies(self):
        return self.trend_replies.all()

    def __str__(self):
        return f'Comment by {self.writer} on {self.trend}'