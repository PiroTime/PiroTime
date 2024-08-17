# Django 모듈
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMessage, send_mail
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.db.models import Count

# 프로젝트 내 모듈
from apps.corboard.forms import CorboardForm, CorCommentForm, CorLetter
from apps.corboard.forms import CorboardForm, CorCommentForm, CorSearchForm
from apps.corboard.models import Corboard, Comment

@login_required
def cor_list(request):
    search_content = request.GET.get('searchContent', '')
    order_by = request.GET.get('order_by', 'date')
    page_number = request.GET.get('page', 1)

    corboards = Corboard.objects.all()

    if search_content:
        corboards = corboards.filter(title__icontains=search_content)

    if order_by == 'likes':
        corboards = corboards.annotate(total_likes=Count('likes__id')).order_by('-total_likes')
    else:
        corboards = corboards.order_by('-date')

    paginator = Paginator(corboards, 6)
    page_obj = paginator.get_page(page_number)

    # 랜덤으로 출력할 사진 list
    image_files = ['back.png', 'back1.png', 'back2.png']

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'corboard/partial_corboard_list.html', {
            'page_obj': page_obj,
            'order_by': order_by,
            'search_content': search_content,
            'image_files': image_files
        })

    return render(request, 'corboard/corboard_list.html', {
        'page_obj': page_obj,
        'order_by': order_by,
        'search_content': search_content,
        'image_files': image_files
    })

@login_required
def cor_create(request):
    if request.method == "POST":
        print("createL post")
        form = CorboardForm(request.POST)
        if form.is_valid():
            cor = form.save(commit = False)
            cor.writer = request.user
            cor.created_at = timezone.now()
            cor.save()

            return redirect('corboard:cor_detail', pk = cor.id)
    else:
        print("create get")

        form = CorboardForm()
        return render(request, 'corboard/corboard_create.html', {'form': form})

@login_required
def cor_detail(request, pk):
    print("cor_detail")
    print(request.method)
    if request.method == 'POST':
        print("POst")
        inp = CorLetter(request.POST)
        if inp.is_valid():
            print("data", inp.cleaned_data['letter'])
            receiver = get_object_or_404(Corboard, pk=pk).writer
            sender = request.user
            subject, message, from_email, recipient_list = generate_email_content(sender, receiver)

            html_message = render_to_string(
                "corboard/message.html",
                {"sender": sender.username, "receiver": receiver.username,
                 "content": f"{receiver.username}님! coorperation에 작성해 주신 프로젝트에 함께 하고 싶은 사람이 있습니다! 아래 링크로 들어와 확인해 보세요!",
                 "message": request.POST.get('letter')},
            )
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                from_email,
                recipient_list,
                html_message=html_message,
            )
            print("++++++++++++")


    cor = get_object_or_404(Corboard, pk=pk)
    form = CorCommentForm()
    content = CorLetter()

    return render(request, 'corboard/corboard_detail.html', {
        'cor': cor,
        'comments': cor.cor_comments.filter(parent=None),
        'form': form,
        'content': content,
    })

@require_POST
@login_required
def cor_delete(request, pk):
    cor = get_object_or_404(Corboard, pk=pk)
    cor.delete()
    return redirect("corboard:cor_list")

@login_required
def cor_update(request, pk):
    cor = get_object_or_404(Corboard, pk=pk)
    if request.method == "GET":
        form = CorboardForm(instance = cor)
    else:
        form = CorboardForm(request.POST, instance=cor)
        if form.is_valid():
            form.save()
            return redirect("corboard:cor_detail", pk=cor.pk)
    return render(request, 'corboard/corboard_update.html', {'form': form})

@login_required
def cor_add_comment(request, pk):
    cor = get_object_or_404(Corboard, pk=pk)
    if request.method == "POST":
        print("==+++++++++++=cor_comment")

        form = CorCommentForm(request.POST)

        if form.is_valid():
            print("==+++++++++++=cor_comment2222")
            comment = form.save(commit=False)
            comment.corboard = cor
            comment.writer = request.user if request.user.is_authenticated else None
            comment.date = timezone.now()

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
            print(form.errors)
            return JsonResponse({'success': False, 'error': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def cor_delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.writer != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
    comment.delete()
    return JsonResponse({'success': True})

@login_required
def cor_like(request,  pk):
    cor = get_object_or_404(Corboard, pk=pk)

    if cor.likes.filter(id=request.user.id).exists():
        cor.likes.remove(request.user.id)
        liked = False
    else:
        cor.likes.add(request.user)
        liked = True

    return JsonResponse({'liked': liked, 'total_likes': cor.total_likes()})

@login_required
def cor_bookmark(request, pk):
    cor = get_object_or_404(Corboard, pk=pk)
    if cor.bookmarks.filter(id=request.user.id).exists():
        cor.bookmarks.remove(request.user.id)
        bookmarked = False
    else:
        cor.bookmarks.add(request.user)
        bookmarked = True
    return JsonResponse({'bookmarked': bookmarked, 'total_likes': cor.total_bookmark()})

@login_required
def cor_search(request):
    query = request.GET.get('searchContent')
    print(query)
    if query:
        result = Corboard.objects.filter(title__icontains=query) | Corboard.objects.filter(content__icontains=query)
    else:
        result = Corboard.objects.none()
    return render(request, 'corboard/corboard_list.html', {'corboards': result})


def generate_email_content(sender, receiver):
    subject = "PiroTime: 협력 제안이 왔습니다!"
    message = f"{sender.username}님으로 부터 협력 제안이 왔습니다. PiroTime에 접속해서 내용을 확인하세요!"
    from_email = 'pirotimeofficial@gmail.com'
    recipient_list = [receiver.email]
    return subject, message, from_email, recipient_list

@login_required
def cor_mail(request, pk):
    letter = CorLetter(request.POST)
    print(letter.letter)
    receiver = get_object_or_404(Corboard, pk=pk).writer
    sender = request.user
    subject, message, from_email, recipient_list = generate_email_content(sender, receiver)

    html_message = render_to_string(
        "corboard/message.html",
        {"sender": sender.username, "receiver": receiver.username,
         "content": f"{receiver.username}님! coorperation에 작성해 주신 프로젝트에 함께 하고 싶은 사람이 있습니다! 아래 링크로 들어와 확인해 보세요!",
         "message": request.POST.get('letter')},
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
    )
    return JsonResponse({'success': True})