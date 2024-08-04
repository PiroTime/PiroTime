from django.contrib import admin

# Register your models here.
from corboard.models import Comment, Corboard

admin.site.register(Comment)
admin.site.register(Corboard)