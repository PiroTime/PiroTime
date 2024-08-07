from django.db import models
from django.urls import reverse
from apps.accounts.models import CustomUser

class Corboard(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    corboardImg = models.ImageField(null=True, blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='cor_likes', blank=True)
    bookmarks = models.ManyToManyField(CustomUser, related_name='cor_bookmarks', blank=True)

    def total_likes(self):
        return self.likes.count()
    def total_bookmark(self):
        return self.bookmarks.count()

    def get_absolute_url(self):
        return reverse('corboard:cor_detail', args=[self.id])

class Comment(models.Model):
    corboard = models.ForeignKey(Corboard, related_name='cor_comments', on_delete=models.CASCADE)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)