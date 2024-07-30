from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    giturl = models.URLField(max_length=200, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='review_likes', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='review_bookmarks', blank=True)

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    
    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.writer} on {self.review}'