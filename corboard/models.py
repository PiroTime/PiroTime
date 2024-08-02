from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Corboard(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    corboardImg = models.ImageField()
    likes = models.ManyToManyField(User, related_name='review_likes', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='review_bookmarks', blank=True)

    def count_like(self):
        return self.likes.count();

class Comment(models.Model):
    corboard = models.ForeignKey(Corboard, related_name='comments', on_delete=models.CASCADE)

    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.writer} on {self.review}'