from django.urls import path
from .views import *

app_name = "review"

urlpatterns = [
    path('', review_list, name='review_list'),
    path('create/', review_create, name='review_create'),
    path('delete/<int:pk>/', review_delete, name='review_delete'),
    path('update/<int:pk>/', review_update, name='review_update'),
    path('detail/<int:pk>/', review_detail, name='review_detail'),
    
    path('comment/<int:pk>/', add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete_comment'),
    
    path('<int:pk>/like/', like_review, name='like_review'),
    path('<int:pk>/bookmark/', bookmark_review, name='bookmark_review'),
]