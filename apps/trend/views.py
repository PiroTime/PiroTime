# Django 내장 모듈
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Count
from django.template.loader import render_to_string

# 프로젝트 내 모듈
from .models import Trend, Comment
from .forms import TrendForm, CommentForm

def trend_list(request):
    search = request.GET.get('search', '')
    order_by = request.GET.get('order_by', 'date')
    page_number = request.GET.get('page', 1)

    trends = Trend.objects.all()

    if search:
        trends = trends.filter(title__icontains=search)

    if order_by == 'likes':
        trends = trends.annotate(total_likes=Count('likes')).order_by('-total_likes')
    else:
        trends = trends.order_by('-date')

    paginator = Paginator(trends, 12)
    page_obj = paginator.get_page(page_number)

    # 랜덤으로 출력할 사진 list
    image_files = ['back.png', 'back1.png', 'back2.png']

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'trend/partial_trend_list.html', {
            'page_obj': page_obj,
            'order_by': order_by,
            'search': search,
            'image_files': image_files
        })

    return render(request, 'trend/trend_list.html', {
        'page_obj': page_obj,
        'order_by': order_by,
        'search': search,
        'image_files': image_files
    })

@login_required
def trend_create(request):
    if request.method == "POST":
        form = TrendForm(request.POST)
        if form.is_valid():
            trend = form.save(commit=False)
            trend.writer = request.user
            trend.created_at = timezone.now()
            trend.save()
            return redirect('trend:trend_detail', pk=trend.pk)
    else:
        form = TrendForm()
    return render(request, 'trend/trend_create.html', {'form': form})

def trend_delete(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
    if trend.writer != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    trend.delete()
    return redirect('trend:trend_list')

def trend_update(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
    
    if request.method == "POST":
        form = TrendForm(request.POST, instance=trend)
        if form.is_valid():
            form.save()
            return redirect('trend:trend_detail', pk=trend.pk)
    else:
        form = TrendForm(instance=trend)
    
    return render(request, 'trend/trend_update.html', {'form': form, 'trend': trend})

@login_required
def trend_detail(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
    comments = trend.comments.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.trend = trend
            comment.writer = request.user if request.user.is_authenticated else None
            comment.created_at = timezone.now()
            comment.save()
            return redirect('trend:trend_detail', pk=trend.pk)

    return render(request, 'trend/trend_detail.html', {
        'trend': trend,
        'comments': comments,
        'comment_form': comment_form,
        'user': request.user,
    })

def add_comment(request, trend_pk):
    trend = get_object_or_404(Trend, pk=trend_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.trend = trend
            comment.writer = request.user if request.user.is_authenticated else None
            comment.created_at = timezone.now()

            # 대댓글일 경우 parent 설정
            parent_id = request.POST.get('parent')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment
            
            comment.save()

            # 댓글 렌더링 HTML
            comment_html = render_to_string('comment_partial.html', {'comment': comment, 'user': request.user})

            return JsonResponse({'success': True, 'comment_html': comment_html})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@csrf_protect
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.writer != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    
    comment.delete()
    return JsonResponse({'success': True})

@login_required
def like_trend(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
    if request.user in trend.likes.all():
        trend.likes.remove(request.user)
        liked = False
    else:
        trend.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': trend.likes.count()})

@login_required
def bookmark_trend(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
    if request.user in trend.bookmarks.all():
        trend.bookmarks.remove(request.user)
        bookmarked = False
    else:
        trend.bookmarks.add(request.user)
        bookmarked = True
    return JsonResponse({'bookmarked': bookmarked})