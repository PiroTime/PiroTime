from django.urls import path
from .views import *

app_name = 'corboard'

urlpatterns = [
    #CRUD
    path('', cor_list, name='cor_list'),
    path('create/', cor_create, name='cor_create'),
    path('detail/<int:pk>/', cor_detail, name='cor_detail'),
    path('delete/<int:pk>/', cor_delete, name='cor_delete'),
    path('update/<int:pk>/', cor_update, name='cor_update'),
    path('like/<int:pk>/', cor_like, name='cor_like'),
    #comment
    path('<int:pk>/comment/', cor_add_comment, name='cor_add_comment'),
    path('comment/delete/<int:pk>/', cor_delete_comment, name='cor_delete_comment'),
    #etc
    path('bookmark/<int:pk>/', cor_bookmark, name='cor_bookmark'),
    path('search/', cor_search, name='cor_search'),
    path('cor_mail/<int:pk>/', cor_mail, name='cor_mail'),
]