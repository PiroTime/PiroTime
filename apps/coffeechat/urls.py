from django.urls import path
from . import views

app_name = 'coffeechat'

urlpatterns = [
    path('', views.home, name='coffeechat_home'), 
]
