from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from .models import Trend, Comment
from .forms import TrendForm, TrendSearchForm, CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def trend_list(request):
    search_form = TrendSearchForm(request.GET)
    query = Q()

    if search_form.is_valid():
        search = search_form.cleaned_data.get('search', '')
        if search:
            query &= Q(title__icontains=search)

    order_by = request.GET.get('order_by', 'date')
    if order_by == 'likes':
        trends = Trend.objects.filter(query).annotate(total_likes=Count('likes')).order_by('-total_likes', '-date')
    else:
        trends = Trend.objects.filter(query).order_by('-date')

    paginator = Paginator(trends, 12)  # 페이지당 12개의 트렌드
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'order_by': order_by,
        'search': search,
    }
    return render(request, 'trend/trend_list.html', context)

def trend_create(request):
    if request.method == "POST":
        form = TrendForm(request.POST)
        if form.is_valid():
            trend = form.save(commit=False)
            trend.writer = request.user if request.user.is_authenticated else None
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

def add_comment(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.trend = trend
            comment.writer = request.user if request.user.is_authenticated else None
            comment.created_at = timezone.now()
            comment.save()
            return redirect('trend:trend_detail', pk=trend.pk)
    else:
        form = CommentForm()
    return render(request, 'trend/trend_detail.html', {'trend': trend, 'comments': trend.comments.all(), 'comment_form': form})

@csrf_exempt
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    trend_pk = comment.trend.pk
    if comment.writer != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    comment.delete()
    return redirect('trend:trend_detail', pk=trend_pk)

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