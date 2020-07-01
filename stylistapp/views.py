from django.shortcuts import render, get_object_or_404,redirect
from django.http  import HttpResponse
from .models import Post

# Create your views here.
def welcome(request):
    return render(request, 'base.html', {})

def post_list_view(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
