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
