from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from coffeechat.models import CoffeeChat, AskCoffeeChat


def main(request):
    return render(request, '/coffeechat/main.html')

def add_bookmark_coffee(request, pk):
    post = get_object_or_404(CoffeeChat, pk=pk)
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user.id)
    else:
        post.bookmarks.add(request.user)
    return redirect('views.main')

#'요청하기' 버튼을 누른다면
def send_email_coffee(request, pk):
    post = get_object_or_404(CoffeeChat, pk=pk)
    receiver = post.user
    asker = request.user

    #reject되는 경우
    if post.status == 'LIMITED':
        return redirect('coffeechat_detail', pk=pk)    #detail으로 reject

    #관련 페이지 작성/수정
    askCoffeeChat = AskCoffeeChat
    askCoffeeChat.username = asker
    askCoffeeChat.receiver = receiver
    askCoffeeChat.created_at = timezone.now()
    askCoffeeChat.post = post
    askCoffeeChat.status = 'stay'

    post.count += 1

    #receiver에게 mail 보내기
    cor_mail(receiver, asker)
    return redirect('coffeechat_detail', pk=pk)

#요청받은 선배님이 거절하는 경우
def rejecting_coffeechat(request, pk):
    receiver = request.user
    askCoffeechat = get_object_or_404(AskCoffeeChat, pk=pk)
    askCoffeechat.status = 'rejected'

    #########
    #sender에게 안내를 보내야 할까요?
    #########

#요청을 수락하는 경우
def accepting_coffeechat(request, pk):
    receiver = request.user
    askCoffeechat = get_object_or_404(AskCoffeeChat, pk=pk)
    askCoffeechat.status = 'acceepted'

    #########
    #sender에게 안내를 보내야 할까요?
    #########

def generate_email_content(sender, receiver):
    subject = "PiroTime: 커피챗 제안이 왔습니다!"
    message = f"{sender.username}님으로 부터 커피챗 제안이 왔습니다. PiroTime에 접속해서 내용을 확인하세요!"
    from_email = 'pirotimeofficial@gmail.com'
    recipient_list = [receiver.email]
    return subject, message, from_email, recipient_list

def cor_mail(receiver, sender):
    subject, message, from_email, recipient_list = generate_email_content(sender, receiver)

    html_message = render_to_string(
        "corboard/message.html",
        {"sender": sender.username, "receiver": receiver.username, "content": "  내용추가  "},
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