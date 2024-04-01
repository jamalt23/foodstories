from django.shortcuts import render
from core.models import *

def home(request):
    posts = Post.objects.order_by('-id')[:4]
    last_post = posts[0]
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'last_post': last_post,
        'categories': categories
    }
    return render(request, 'index.html', context=context)

def detail(request, id):
    post = Post.objects.get(id=id)
    posts = Post.objects.order_by('-id')[:3]
    posts = [item for item in posts if not item==post]

    tags = Tag.objects.all()
    categories = Category.objects.all()

    # tag_count = Tag.objects.all().count
    context = {
        'post': post,
        'tags': tags,
        'categories': categories,
        'posts': posts,
        # 'tag_count': tag_count
    }
    return render(request, 'single.html', context=context)
