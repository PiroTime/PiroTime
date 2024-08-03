from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from coffeechat.models import CoffeeChat


def main(request):
    return render(request, '/coffeechat/main.html')

def add_bookmark_coffee(request, pk):
    post = get_object_or_404(CoffeeChat, pk=pk)
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user.id)
    else:
        post.bookmarks.add(request.user)
    return redirect('views.main')

def send_email_coffee(request, pk):
    post = get_object_or_404(CoffeeChat, pk=pk)

    if post.count > 10:
        return redirect('views.main')       #detail 페이지로 던져야
    post.count += 1
    post.status = 'WAITING'


def cor_mail(request, pk):
    receiver = get_object_or_404(CoffeeChat, pk=pk).username
    sender = request.user

    subject, message, from_email, recipient_list = generate_email_content(sender, receiver)
    EmailMessage(subject=subject, from_email=from_email, to=recipient_list, body=message).send()
    return HttpResponse('Email sent successfully')


def generate_email_content(sender, receiver):
    subject = "CoffeeChat 친청이 왔습니다."
    message = f"{sender.username}님으로 부터 협력 제안이 왔습니다. PiroTime에 접속해서 내용을 확인하세요!"
    from_email = 'pirotimeofficial@gmail.com'
    recipient_list = [receiver.email]
    return subject, message, from_email, recipient_list