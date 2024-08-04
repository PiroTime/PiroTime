
from django.db import models

# Create your models here.
from accounts.models import CustomUser


class Corboard(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    corboardImg = models.ImageField(null=True, blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='cor_likes', blank=True)
    bookmarks = models.ManyToManyField(CustomUser, related_name='cor_bookmarks', blank=True)

    def count_like(self):
        return self.likes.count();

class Comment(models.Model):
    corboard = models.ForeignKey(Corboard, related_name='cor_comments', on_delete=models.CASCADE)

    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

