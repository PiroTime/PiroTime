from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='coffeechat_main'),
    path('list/', views.list, name='coffeechat_list'),
    path('create/', views.create, name='coffeechat_create'),
    path('detail/<int:pk>/', views.detail, name='coffeechat_detail'),
    path('update/<int:pk>/', views.update, name='coffeechat_update'),
    path('delete/<int:pk>/', views.delete, name='coffeechat_delete'),
]
