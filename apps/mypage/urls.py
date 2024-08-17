from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('ajax/activities/', views.ActivitiesAjaxView.as_view(), name='ajax_activities'),  # AJAX
    path('ajax/profile-modal/', views.profile_modal_view, name='profile_modal'),
    path('profile/<int:user_id>/', views.profile_read, name='profile_read'),
    path('bookmark/<int:pk>/', views.coffeechat_bookmark_profile, name='coffeechat_bookmark_profile'),
]