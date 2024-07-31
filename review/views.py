from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

def review_list(request):
    reviews = Review.objects.all()
    filter_by = request.GET.get('filter', 'date')
    if filter_by == 'likes':
        reviews = reviews.annotate(like_count=models.Count('likes')).order_by('-like_count', '-date')
    else:
        reviews = reviews.order_by('-date')
    return render(request, 'review/review_list.html', {'reviews': reviews})

def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            
            #review.writer = request.user
            review.writer = request.user if request.user.is_authenticated else None
            
            review.date = timezone.now()
            review.save()
            return redirect('review:review_detail', pk=review.pk)
    else:
        form = ReviewForm()
    return render(request, 'review/review_create.html', {'form': form})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('review:review_list')

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review:review_detail', pk=review.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'review/review_create.html', {'form': form})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    comments = review.comments.all()
    comment_form = CommentForm()
    return render(request, 'review/review_detail.html', {'review': review, 'comments': comments, 'comment_form': comment_form})

def add_comment(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.writer = request.user if request.user.is_authenticated else None
            comment.date = timezone.now()
            comment.save()
            return redirect('review:review_detail', pk=review.pk)
    else:
        form = CommentForm()
    return render(request, 'review/review_detail.html', {'review': review, 'comments': review.comments.all(), 'comment_form': form})

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    review_pk = comment.review.pk
    if comment.writer != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    comment.delete()
    return redirect('review:review_detail', pk=review_pk)

def like_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.likes.filter(id=request.user.id).exists():
        review.likes.remove(request.user)
    else:
        review.likes.add(request.user)
    return HttpResponseRedirect(reverse('review:review_detail', args=[pk]))

def bookmark_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.bookmarks.filter(id=request.user.id).exists():
        review.bookmarks.remove(request.user)
    else:
        review.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('review:review_detail', args=[pk]))