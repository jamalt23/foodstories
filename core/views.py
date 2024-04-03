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

    context = {
        'post': post,
        'tags': tags,
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'single.html', context=context)

def about(request):
    return render(request, 'about.html')

def stories(request, category="all"):
    if category==None: category="all"
    if category=="all":
        posts = Post.objects.order_by('-id')
        category = "All"
    else:
        posts = Post.objects.filter(category__title=category).order_by('-id')
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
        'category': category
    }
    return render(request, 'stories.html', context=context)

def recipes(request):
    return render(request, 'recipes.html')

def contact(request):
    return render(request, 'contact.html')