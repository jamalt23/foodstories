from django.shortcuts import render
from django.http import HttpRequest
from core.models import *
import re

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

def extract_param(url: str, key: str):
    search = re.search(f"{key}=([^&]*)", url)
    if search:
        return search.group(1)

def stories(request:HttpRequest, tag=None, category=None):
    # tag = request.GET.get('tag')
    # category = request.GET.get('category')
    tag = extract_param(request.path, 'tag')
    category = extract_param(request.path, 'category')
    if tag==None: tag="all"
    if category==None: category="all"
    if tag=="all" and category=="all":
        posts = Post.objects.order_by('-id')
    elif category!="all" and tag=="all":
        posts = Post.objects.filter(category__title=category).order_by('-id')
    elif tag != "all" and category=="all":
        posts = Post.objects.order_by('-id')
        posts = [post for post in posts if tag.title() in post.get_tags()]
    else:
        posts = Post.objects.filter(category__title=category).order_by('-id')
        posts = [post for post in posts if tag in post.get_tags()]

    # print(f"tag: {tag}, category: {category}")

    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
        'category': category,
        'tag': tag
    }
    return render(request, 'stories.html', context=context)

def recipes(request):
    return render(request, 'recipes.html')

def contact(request):
    return render(request, 'contact.html')