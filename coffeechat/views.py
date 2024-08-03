from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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

    post.count += 1
    post.status = 'WAITING'



def generate_email_content(sender, receiver):
    subject = "PiroTime: 커피챗 제안이 왔습니다!"
    message = f"{sender.username}님으로 부터 커피챗 제안이 왔습니다. PiroTime에 접속해서 내용을 확인하세요!"
    from_email = 'pirotimeofficial@gmail.com'
    recipient_list = [receiver.email]
    return subject, message, from_email, recipient_list

def cor_mail(request, pk):
    receiver = get_object_or_404(CoffeeChat, pk=pk).writer
    sender = request.user
    subject, message, from_email, recipient_list = generate_email_content(sender, receiver)

    html_message = render_to_string(
        "corboard/message.html",
        {"sender": sender.username, "receiver": receiver.username},
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
    )
    return HttpResponse('Email sent successfully')