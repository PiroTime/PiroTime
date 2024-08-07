from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('ajax/activities/', views.ActivitiesAjaxView.as_view(), name='ajax_activities'),  # AJAX
]