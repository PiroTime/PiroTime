from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import CoffeeChat, Hashtag, CoffeeChatRequest
from .forms import CoffeeChatForm
from datetime import timedelta
import json

def home(request):
    return render(request, 'coffeechat/home.html')

def list(req):
    query = req.GET.get('search')
    if query:
        profiles = CoffeeChat.objects.filter(
            hashtags__name__icontains(query)
        ).distinct()
    else:
        profiles = CoffeeChat.objects.all()
    
    ctx = {
        "profiles": profiles
    }
    return render(req, 'coffeechat/list.html', ctx)

@login_required
def create(req):
    # 현재 사용자가 이미 프로필을 가지고 있는지 확인
    existing_profile = CoffeeChat.objects.filter(receiver=req.user).first()
    if existing_profile:
        return redirect('coffeechat:coffeechat_detail', pk=existing_profile.pk)  # 이미 존재하면 자신의 detail 페이지로 리디렉션

    if req.method == "POST": #생성 후
        form = CoffeeChatForm(req.POST)
        if form.is_valid():
            coffeechat = form.save(commit=False)
            coffeechat.receiver = req.user
            coffeechat.count = 0  # count 기본값 설정
            coffeechat.content = form.cleaned_data['content']
            coffeechat.save()
            
            # 해시태그 저장
            hashtags = form.cleaned_data['hashtags']
            hashtag_list = json.loads(hashtags)
            hashtag_objects = []
            for tag in hashtag_list:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                hashtag_objects.append(hashtag)
            coffeechat.hashtags.set(hashtag_objects)
            
            coffeechat.save()
            return redirect('coffeechat:coffeechat_detail', pk=coffeechat.pk)
    else: #생성 전(GET)
        form = CoffeeChatForm()
    ctx = {
        'form': form
    }
    return render(req, 'coffeechat/create.html', ctx)

def detail(request, pk):
    profile = CoffeeChat.objects.get(pk=pk)
    if request.method == "POST" and request.user != profile.receiver:
        existing_request = CoffeeChatRequest.objects.filter(user=request.user, coffeechat=profile).exists()
        
        if not existing_request:
            start_of_day = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            daily_requests = CoffeeChatRequest.objects.filter(
                coffeechat__receiver=profile.receiver,
                created_at__range=(start_of_day, end_of_day),
                status='WAITING'
            ).count()

            if daily_requests < 5: # 아직 커피챗 가능
                CoffeeChatRequest.objects.create(
                    user=request.user,
                    coffeechat=profile,
                    status='WAITING'
                )
            else: # 커피챗 불가 -> 상태변경
                profile.status = 'LIMITED'
                profile.save()
    
    # 현재 로그인한 사람이 username이고, receiver, status를 통해서 filter 후 존재확인 -> 있으면 제안하기 버튼을 현재 수락대기중으로 변경
    is_waiting = CoffeeChatRequest.objects.filter(user=request.user, coffeechat=profile, status='WAITING').exists()
    # 커피챗 받은 수 계산
    waiting_requests = CoffeeChatRequest.objects.filter(coffeechat__receiver=profile.receiver, status='WAITING').count()
    is_limited = waiting_requests >= 5 and not is_waiting
    hashtags = profile.hashtags.all()

    # 해당 프로필에 대한 모든 요청을 가져옵니다.
    requests = CoffeeChatRequest.objects.filter(coffeechat=profile)

    ctx = {
        'profile': profile,
        'is_waiting': is_waiting,
        'is_limited': is_limited,
        'hashtags': hashtags,
        'requests': requests  # 요청 목록을 컨텍스트에 추가
    }
    return render(request, 'coffeechat/detail.html', ctx)

@login_required
def accept_request(request, request_id): #수락 시 
    coffeechat_request = CoffeeChatRequest.objects.get(id=request_id)
    if request.user == coffeechat_request.coffeechat.receiver:
        coffeechat_request.status = 'ACCEPTED'
        coffeechat_request.save()
        
        # CoffeeChat 모델의 count 필드 증가
        coffeechat = coffeechat_request.coffeechat
        coffeechat.count += 1
        coffeechat.save()
        
    return redirect('coffeechat:coffeechat_detail', pk=coffeechat_request.coffeechat.pk)

@login_required
def update(req, pk):
    profile = CoffeeChat.objects.get(pk=pk)
    if req.method == "POST": # 수정 후
        form = CoffeeChatForm(req.POST, instance=profile)
        if form.is_valid():
            coffeechat = form.save(commit=False)
            coffeechat.receiver = req.user
            coffeechat.count = 0  # count 필드에 기본값 설정
            coffeechat.content = form.cleaned_data['content']
            coffeechat.save()
            
            # 해시태그 저장
            hashtags = form.cleaned_data['hashtags']
            hashtag_list = json.loads(hashtags)
            hashtag_objects = []
            for tag in hashtag_list:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                hashtag_objects.append(hashtag)
            coffeechat.hashtags.set(hashtag_objects)
            
            coffeechat.save()
            return redirect('coffeechat:coffeechat:coffeechat_detail', pk=profile.pk)
    else: # 수정 전(위한 load, GET)
        form = CoffeeChatForm(instance=profile)
        # 수정을 위해서 기존 콘텐츠와 해시태그 로드(JSON)
        initial_hashtags = json.dumps([{'value': hashtag.name} for hashtag in profile.hashtags.all()])
        form.fields['hashtags'].initial = initial_hashtags
        form.fields['content'].initial = profile.content

    ctx = {
        'form': form,
        'profile': profile
    }
    return render(req, 'coffeechat/update.html', ctx)

@login_required
def delete(req, pk):
    profile = CoffeeChat.objects.get(pk=pk)
    if req.method == "POST":
        profile.delete()
        return redirect('coffeechat:coffeechat_list')
    ctx = {
        'profile': profile
    }
    return render(req, 'coffeechat/delete.html', ctx)