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
