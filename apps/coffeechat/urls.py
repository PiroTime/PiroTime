from django.urls import path
from . import views

app_name = 'coffeechat'

urlpatterns = [
    path('', views.home, name='coffeechat_home'), 
    path('list/', views.list, name='coffeechat_list'),
    path('create/', views.create, name='coffeechat_create'),
    path('detail/<int:pk>/', views.detail, name='coffeechat_detail'),
    path('update/<int:pk>/', views.update, name='coffeechat_update'),
    path('delete/<int:pk>/', views.delete, name='coffeechat_delete'),
    path('accept_request/<int:request_id>/', views.accept_request, name='accept_request'),
]
