from django.urls import path
from .views import *

app_name = "trend"

urlpatterns = [
    path('', trend_list, name='trend_list'),
    path('create/', trend_create, name='trend_create'),
    path('delete/<int:pk>/', trend_delete, name='trend_delete'),
    path('update/<int:pk>/', trend_update, name='trend_update'),
    path('detail/<int:pk>/', trend_detail, name='trend_detail'),
    
    path('comment/<int:pk>/', add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete_comment'),
    
    path('<int:pk>/like/', like_trend, name='like_trend'),
    path('<int:pk>/bookmark/', bookmark_trend, name='bookmark_trend'),
]