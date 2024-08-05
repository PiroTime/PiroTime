from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('my_posts/', views.MyPostsView.as_view(), name='my_posts'),
    path('liked_posts/', views.LikedPostsView.as_view(), name='liked_posts'),
    path('bookmarked_posts/', views.BookmarkedPostsView.as_view(), name='bookmarked_posts'),
    path('commented_posts/', views.CommentedPostsView.as_view(), name='commented_posts'),
]