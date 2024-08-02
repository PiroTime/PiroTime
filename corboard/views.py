from datetime import timezone

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from corboard.forms import CorboardForm, CorCommentForm
from corboard.models import Corboard, Comment
from django.contrib.auth.decorators import login_required
# Create your views here.

def cor_list(request):
    cors = Corboard.objects.all()

    return render(request, 'corboard/corboard_list.html', {'corboards': cors})


def cor_create(request):
    if request.method == "POST":
        print("createL post")
        form = CorboardForm(request.POST)
        if form.is_valid():
            cor = form.save(commit = False)
            cor.writer = request.user
            cor.date = timezone.now()
            cor.save()
            print("cor_create: form valid")
            return redirect('corboard:cor_detail', pk = cor.id)
    else:
        print("createL get")

        form = CorboardForm()
        return render(request, 'corboard/corboard_create.html', {'form': form})

def cor_detail(request, pk):
    print("cor_detail")
    cor = get_object_or_404(Corboard, pk=pk)
    return render(request, 'corboard/corboard_detail.html', {'cor':cor, 'comments': cor.comments.all(), 'commentForm':CorCommentForm()})

@require_POST
def cor_delete(request, pk):
    cor = get_object_or_404(Corboard, pk=pk)
    cor.delete()
    return redirect("corboard:corboard_list")

def cor_update(request, pk):
    cor = get_object_or_404(Corboard, pk=pk)
    if request.method == "GET":
        form = CorboardForm(instance = cor)
    else:
        form = CorboardForm(request.POST, instance=cor)
        if form.is_vaild():
            form.save()
            return redirect("corboard:corboard_detail", pk=form.id)
    return render(request, 'corboard/corboard_update.html', {'form': form})

@login_required
def cor_add_comment(request, pk):
    cor  = get_object_or_404(Corboard, pk=pk)
    if request.method == "POST":
        form = CorCommentForm(request.POST)
        if form.is_vaild():
            comment = form.save(commit=False)
            comment.date = timezone.now()
            comment.corboard = cor
            comment.writer = request.user
            comment.save()
            return redirect('corboard:corboard_detail', pk = cor.id)
    else:
        commentForm = CorCommentForm()
    return render(request, 'corboard/corboard_detail', {'cor': cor, 'comments': cor.comments.all(), 'commentForm':commentForm})

def cor_delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    corboard_id = comment.corboard.id
    if comment.writer == request.user:
        comment.delete()
    return redirect('corboard:corboard_detail', pk=corboard_id)

def cor_like(request,  pk):
    cor = get_object_or_404(Corboard, pk=pk)
    if cor.likes.filter(id=request.user.id).exists():
        cor.likes.remove(request.user.id)
    else:
        cor.likes.add(request.user)
    return HttpResponseRedirect(reverse('corboard:corboard_detail', args=[pk]))

def cor_bookmark(request, pk):
    cor = get_object_or_404(Corboard, pk=pk)
    if cor.bookmarks.filter(id=request.user.id).exists():
        cor.bookmarks.remove(request.user.id)
    else:
        cor.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('corboard:corboard_detail', args=[pk]))

def cor_search(request):
    query = request.GET.get('searchContent')
    if query:
        result = Corboard.objects.filter(title__icontains=query) | Corboard.objects.filter(content__icontains=query)
    else:
        result = Corboard.objects.none()
    return render(request, 'corboard/corboard_list.html', {'corboards': result})

def cor_mail(request, pk):
    receiver = get_object_or_404(Corboard, pk=pk).writer
    sender = request.user

    if request.method == 'POST':

        subject, message, from_email, recipient_list = generate_email_content(sender, receiver)
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        return HttpResponse('Email sent successfully')
    return render(request, 'send_email.html')

def generate_email_content(sender, receiver):
    subject = "PiroTime: 협력 제안이 왔습니다!"
    message = f"{sender.username}님으로 부터 협력 제안이 왔습니다. PiroTime에 접속해서 내용을 확인하세요!"
    from_email = 'pirotimeofficial@gmail.com'
    recipient_list = [receiver.email]
    return subject, message, from_email, recipient_list

