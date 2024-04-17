from django.shortcuts import render, redirect
from django.http import HttpRequest
from core.models import *
from core.forms import PostForm
import re

def home(request):
    if request.method == 'POST':
        subscriber_email = request.POST.get('subscriber_email')
        subscriber = Subscribe(email=subscriber_email)
        subscriber.save()
    
    posts = Post.objects.order_by('-id')[:4]
    if request.user.is_authenticated:
        myposts = request.user.posts.order_by('-id')[:4]
    else:
        myposts = []
    last_post = posts[0]
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'last_post': last_post,
        'categories': categories,
        'myposts': myposts
    }
    return render(request, 'index.html', context=context)

def detail(request, id):
    post = Post.objects.get(id=id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        comment = Comment(author=request.user, text=comment_text, post=post)
        comment.save()
        return redirect('core:detail', id=id)

    posts = Post.objects.order_by('-id')[:3]
    posts = [item for item in posts if not item==post]

    tags = Tag.objects.all()
    categories = Category.objects.all()

    context = {
        'post': post,
        'tags': tags,
        'categories': categories,
        'posts': posts
    }
    return render(request, 'single.html', context=context)

def about(request):
    return render(request, 'about.html')

def extract_param(url: str, key: str):
    search = re.search(f"{key}=([^&]*)", url)
    if search:
        return search.group(1)

def stories(request:HttpRequest, tag=None, category=None):
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

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('core:home')
    form = PostForm()
    return render(request, 'create_story.html', {'form': form})
