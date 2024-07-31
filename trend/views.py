from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Trend, Comment
from .forms import TrendForm, CommentForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

def trend_list(request):
    trends = Trend.objects.all()
    filter_by = request.GET.get('filter', 'date')
    if filter_by == 'likes':
        trends = trends.annotate(like_count=models.Count('likes')).order_by('-like_count', '-date')
    else:
        trends = trends.order_by('-date')
    return render(request, 'trend/trend_list.html', {'trends': trends})

def trend_create(request):
    if request.method == "POST":
        form = TrendForm(request.POST)
        if form.is_valid():
            trend = form.save(commit=False)
            
            #trend.writer = request.user
            trend.writer = request.user if request.user.is_authenticated else None
            
            trend.date = timezone.now()
            trend.save()
            return redirect('trend:trend_detail', pk=trend.pk)
    else:
        form = TrendForm()
    return render(request, 'trend/trend_create.html', {'form': form})

def trend_delete(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
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
    return render(request, 'trend/trend_create.html', {'form': form})

def trend_detail(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
    comments = trend.comments.all()
    comment_form = CommentForm()
    return render(request, 'trend/trend_detail.html', {'trend': trend, 'comments': comments, 'comment_form': comment_form})

def add_comment(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.trend = trend
            comment.writer = request.user if request.user.is_authenticated else None
            comment.date = timezone.now()
            comment.save()
            return redirect('trend:trend_detail', pk=trend.pk)
    else:
        form = CommentForm()
    return render(request, 'trend/trend_detail.html', {'trend': trend, 'comments': trend.comments.all(), 'comment_form': form})

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    trend_pk = comment.trend.pk
    if comment.writer != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    comment.delete()
    return redirect('trend:trend_detail', pk=trend_pk)

def like_trend(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
    if trend.likes.filter(id=request.user.id).exists():
        trend.likes.remove(request.user)
    else:
        trend.likes.add(request.user)
    return HttpResponseRedirect(reverse('trend:trend_detail', args=[pk]))

def bookmark_trend(request, pk):
    trend = get_object_or_404(Trend, pk=pk)
    if trend.bookmarks.filter(id=request.user.id).exists():
        trend.bookmarks.remove(request.user)
    else:
        trend.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('trend:trend_detail', args=[pk]))