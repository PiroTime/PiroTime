from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import UserProfile
from apps.trend.models import Trend, Comment as TrendComment
from apps.review.models import Review, Comment as ReviewComment
from apps.accounts.forms import CustomUserChangeForm
from apps.accounts.models import CustomUser

# 프로필 보기 뷰
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'], created = UserProfile.objects.get_or_create(user=self.request.user)
        return context

# 프로필 수정 뷰
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'mypage/profile_edit.html'
    success_url = reverse_lazy('mypage:profile')

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, pk=self.request.user.pk)

# 내가 작성한 글 보기 뷰
class MyPostsView(LoginRequiredMixin, ListView):
    template_name = 'mypage/my_posts.html'
    context_object_name = 'my_posts'

    def get_queryset(self):
        trend_posts = Trend.objects.filter(writer=self.request.user)
        review_posts = Review.objects.filter(writer=self.request.user)
        return list(trend_posts) + list(review_posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_posts'] = [{'post': post, 'type': 'Trend' if isinstance(post, Trend) else 'Review'} for post in context['my_posts']]
        return context

# 내가 좋아요한 글 보기 뷰
class LikedPostsView(LoginRequiredMixin, ListView):
    template_name = 'mypage/liked_posts.html'
    context_object_name = 'liked_posts'

    def get_queryset(self):
        liked_trends = Trend.objects.filter(likes=self.request.user)
        liked_reviews = Review.objects.filter(likes=self.request.user)
        return list(liked_trends) + list(liked_reviews)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_posts'] = [{'post': post, 'type': 'Trend' if isinstance(post, Trend) else 'Review'} for post in context['liked_posts']]
        return context

# 내가 북마크한 글 보기 뷰
class BookmarkedPostsView(LoginRequiredMixin, ListView):
    template_name = 'mypage/bookmarked_posts.html'
    context_object_name = 'bookmarked_posts'

    def get_queryset(self):
        bookmarked_trends = Trend.objects.filter(bookmarks=self.request.user)
        bookmarked_reviews = Review.objects.filter(bookmarks=self.request.user)
        return list(bookmarked_trends) + list(bookmarked_reviews)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmarked_posts'] = [{'post': post, 'type': 'Trend' if isinstance(post, Trend) else 'Review'} for post in context['bookmarked_posts']]
        return context

# 내가 댓글을 단 글 보기 뷰
class CommentedPostsView(LoginRequiredMixin, ListView):
    template_name = 'mypage/commented_posts.html'
    context_object_name = 'commented_posts'

    def get_queryset(self):
        commented_trend_ids = TrendComment.objects.filter(writer=self.request.user).values_list('trend_id', flat=True)
        commented_review_ids = ReviewComment.objects.filter(writer=self.request.user).values_list('review_id', flat=True)

        commented_trends = Trend.objects.filter(id__in=commented_trend_ids)
        commented_reviews = Review.objects.filter(id__in=commented_review_ids)

        return list(commented_trends) + list(commented_reviews)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commented_posts'] = [{'post': post, 'type': 'Trend' if isinstance(post, Trend) else 'Review'} for post in context['commented_posts']]
        return context
