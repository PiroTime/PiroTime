# Django 내장 모듈
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseForbidden, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q

# 프로젝트 내 모듈
from .models import Review, Comment
from .forms import ReviewForm, CommentForm, ReviewSearchForm


def review_list(request):
    search = request.GET.get('search', '')
    search_form = ReviewSearchForm(request.GET)
    query = Q()

    if search_form.is_valid():
        search = search_form.cleaned_data.get('search', '')
    if search:
            query &= Q(title__icontains=search)

    order_by = request.GET.get('order_by', 'date')
    page_number = request.GET.get('page', 1)

    reviews = Review.objects.all()

    if search:
        reviews = reviews.filter(title__icontains=search)

    if order_by == 'likes':
        reviews = reviews.annotate(total_likes=Count('likes')).order_by('-total_likes')
    else:
        reviews = reviews.order_by('-date')

    paginator = Paginator(reviews, 6)
    page_obj = paginator.get_page(page_number)

    # 랜덤으로 출력할 사진 list
    image_files = ['back.png', 'back1.png', 'back2.png']

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'review/partial_review_list.html', {
            'page_obj': page_obj,
            'order_by': order_by,
            'search': search,
            'image_files': image_files
        })

    return render(request, 'review/review_list.html', {
        'page_obj': page_obj,
        'order_by': order_by,
        'search': search,
        'image_files': image_files
    })

def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.writer = request.user if request.user.is_authenticated else None
            review.created_at = timezone.now()
            review.save()
            return redirect('review:review_detail', pk=review.pk)
    else:
        form = ReviewForm()
    return render(request, 'review/review_create.html', {'form': form})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.writer != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
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
    
    return render(request, 'review/review_update.html', {'form': form, 'review': review})

@login_required
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    comments = review.comments.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.writer = request.user if request.user.is_authenticated else None
            comment.created_at = timezone.now()
            comment.save()
            return redirect('review:review_detail', pk=review.pk)

    return render(request, 'review/review_detail.html', {
        'review': review,
        'comments': comments,
        'comment_form': comment_form,
        'user': request.user,
    })

def add_comment(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.writer = request.user if request.user.is_authenticated else None
            comment.created_at = timezone.now()
            # 대댓글일 경우 parent 설정
            parent_id = request.POST.get('parent')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment
            else:
                comment.parent = None
            
            comment.save()
            if comment.parent:
                return redirect(f'{comment.review.get_absolute_url()}#comment-{comment.id}')
            else:
                return redirect('review:review_detail', pk=review.pk)
    else:
        form = CommentForm()
    return render(request, 'review/review_detail.html', {'review': review, 'comments': review.comments.all(), 'comment_form': form})

@csrf_exempt
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    review_pk = comment.review.pk
    if comment.writer != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    comment.delete()
    return redirect('review:review_detail', pk=review_pk)

@login_required
def like_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user in review.likes.all():
        review.likes.remove(request.user)
        liked = False
    else:
        review.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'total_likes': review.likes.count()})

@login_required
def bookmark_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user in review.bookmarks.all():
        review.bookmarks.remove(request.user)
        bookmarked = False
    else:
        review.bookmarks.add(request.user)
        bookmarked = True
    return JsonResponse({'bookmarked': bookmarked})