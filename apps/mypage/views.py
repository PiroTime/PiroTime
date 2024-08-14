# Django 내장 모듈
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# 프로젝트 내 모듈
from apps.accounts.models import CustomUser
from apps.accounts.forms import CustomUserChangeForm
from apps.review.models import Review, Comment as ReviewComment
from apps.corboard.models import Corboard, Comment as CorboardComment
from apps.trend.models import Trend, Comment as TrendComment
from apps.coffeechat.models import CoffeeChat, CoffeeChatRequest

# 프로필 보기 뷰
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context

# 프로필 수정 뷰
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'mypage/profile_edit.html'
    success_url = reverse_lazy('mypage:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        # messages.success(self.request, '프로필이 성공적으로 업데이트되었습니다.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, '오류가 발생했습니다. 입력 내용을 다시 확인해 주세요.')
        return super().form_invalid(form)

# AJAX
class ActivitiesAjaxView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        filter_type = request.GET.get('filter', 'my_posts')
        category = request.GET.get('category', 'all')
        user_id = request.GET.get('user_id', None)

        # 특정 사용자 글 필터링하기 위해 user_id 사용
        if user_id:
            target_user = get_object_or_404(CustomUser, id=user_id)
        else:
            target_user = request.user

        # 내가 쓴 글 필터링
        if filter_type == 'my_posts':
            if category == 'review':
                posts = Review.objects.filter(writer=target_user)
            elif category == 'trend':
                posts = Trend.objects.filter(writer=target_user)
            elif category == 'corboard':
                posts = Corboard.objects.filter(writer=target_user)
            else:
                posts = list(Trend.objects.filter(writer=target_user)) + \
                        list(Review.objects.filter(writer=target_user)) + \
                        list(Corboard.objects.filter(writer=target_user))

        # 내가 북마크한 글 필터링
        elif filter_type == 'bookmarked':
            if category == 'review':
                posts = Review.objects.filter(bookmarks=target_user)
            elif category == 'trend':
                posts = Trend.objects.filter(bookmarks=target_user)
            elif category == 'corboard':
                posts = Corboard.objects.filter(bookmarks=target_user)
            elif category == 'coffeechat':
                posts = CoffeeChat.objects.filter(bookmarks=target_user)
            else:
                posts = list(Trend.objects.filter(bookmarks=target_user)) + \
                        list(Review.objects.filter(bookmarks=target_user)) + \
                        list(Corboard.objects.filter(bookmarks=target_user)) + \
                        list(CoffeeChat.objects.filter(bookmarks=target_user))

        # 내가 좋아요한 글 필터링
        elif filter_type == 'liked':
            if category == 'review':
                posts = Review.objects.filter(likes=target_user)
            elif category == 'trend':
                posts = Trend.objects.filter(likes=target_user)
            elif category == 'corboard':
                posts = Corboard.objects.filter(likes=target_user)
            else:
                posts = list(Trend.objects.filter(likes=target_user)) + \
                        list(Review.objects.filter(likes=target_user)) + \
                        list(Corboard.objects.filter(likes=target_user))

        # 내가 댓글을 단 글 필터링
        elif filter_type == 'commented':
            if category == 'review':
                post_ids = ReviewComment.objects.filter(writer=target_user).values_list('review_id', flat=True)
                posts = Review.objects.filter(id__in=post_ids)
            elif category == 'trend':
                post_ids = TrendComment.objects.filter(writer=target_user).values_list('trend_id', flat=True)
                posts = Trend.objects.filter(id__in=post_ids)
            elif category == 'corboard':
                post_ids = CorboardComment.objects.filter(writer=target_user).values_list('corboard_id', flat=True)
                posts = Corboard.objects.filter(id__in=post_ids)
            else:
                trend_ids = TrendComment.objects.filter(writer=target_user).values_list('trend_id', flat=True)
                review_ids = ReviewComment.objects.filter(writer=target_user).values_list('review_id', flat=True)
                corboard_ids = CorboardComment.objects.filter(writer=target_user).values_list('corboard_id', flat=True)
                posts = list(Trend.objects.filter(id__in=trend_ids)) + \
                        list(Review.objects.filter(id__in=review_ids)) + \
                        list(Corboard.objects.filter(id__in=corboard_ids))

        # 커피챗 필터링
        elif filter_type == 'coffeechat':
            if category == 'requests_sent':
                requests_sent = CoffeeChatRequest.objects.filter(user=target_user, status='WAITING')
                data = [{
                    'receiver': request.coffeechat.receiver.username,
                    'job': request.coffeechat.job,
                    'created_at': request.created_at.isoformat(),
                    'status': request.get_status_display(),
                } for request in requests_sent]
                return JsonResponse({'requests_sent': data})

            elif category == 'requests_received':
                requests_received = CoffeeChatRequest.objects.filter(coffeechat__receiver=target_user, status='WAITING')
                data = [{
                    'sender': request.user.username,
                    'job': request.coffeechat.job,
                    'created_at': request.created_at.isoformat(),
                    'status': request.get_status_display(),
                    'accept_url': reverse_lazy('coffeechat:accept_request', args=[request.id]),
                    'reject_url': reverse_lazy('coffeechat:reject_request', args=[request.id]),
                } for request in requests_received]
                return JsonResponse({'requests_received': data})
            
            elif category == 'bookmarked':
                bookmarked_coffeechats = CoffeeChat.objects.filter(bookmarks=target_user)
                data = [{
                    'receiver': coffeechat.receiver.username,
                    'job': coffeechat.job,
                    'created_at': coffeechat.created_at.isoformat(),
                    'content': coffeechat.content,
                } for coffeechat in bookmarked_coffeechats]
                return JsonResponse({'bookmarked_coffeechats': data})
            
            elif category == 'history':
                accepted_requests = CoffeeChatRequest.objects.filter(coffeechat__receiver=target_user, status='ACCEPTED')
                data = [{
                    'sender': request.user.username,
                    'job': request.coffeechat.job,
                    'created_at': request.created_at.isoformat(),
                    'status': request.get_status_display(),
                    'review': {
                        'rating': request.review.rating if hasattr(request, 'review') else None,
                        'content': request.review.content if hasattr(request, 'review') else None,
                        'created_at': request.review.created_at.isoformat() if hasattr(request, 'review') else None,
                    } if hasattr(request, 'review') else None,
                } for request in accepted_requests]
                return JsonResponse({'accepted_requests': data})

        # 내 정보 보기
        elif filter_type == 'profile_info':
            user = target_user
            data = {
                'username': user.username,
                'email': user.email,
                'nickname': user.nickname,
                'profile_image': user.profile_image.url if user.profile_image else None,
                'cohort': user.cohort,
                'intro': user.intro,
            }
            return JsonResponse(data)

        else:
            posts = list(Trend.objects.filter(writer=target_user)) + \
                    list(Review.objects.filter(writer=target_user)) + \
                    list(Corboard.objects.filter(writer=target_user))

        posts_data = [{
            'title': post.title, 
            'content': post.content[:100],
            'writer': post.writer.username,
            'writer_id': post.writer.id,
            'date': post.date.isoformat(),
            'url': post.get_absolute_url(),
            'category': getattr(post, 'category', '일반')
        } for post in posts]

        return JsonResponse({'posts': posts_data})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user

        # 랜덤으로 출력할 사진 리스트
        image_files = ['back.png', 'back1.png', 'back2.png']
        context['image_files'] = image_files

        return context

import random

def profile_read(request, user_id):
    User = get_user_model()
    user_profile = get_object_or_404(User, pk=user_id)
    
    # 랜덤으로 출력할 사진 리스트
    image_files = ['back.png', 'back1.png', 'back2.png']
    random_image = random.choice(image_files)

    return render(request, 'mypage/profile_read.html', {
        'profile_user': user_profile,
        'random_image': random_image,
    })