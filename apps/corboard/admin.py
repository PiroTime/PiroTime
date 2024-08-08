from django.contrib import admin

# Register your models here.
from apps.corboard.models import Comment, Corboard

admin.site.register(Comment)
admin.site.register(Corboard)