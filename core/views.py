import re
from django.shortcuts import render, redirect
from django.http import *
from core.models import *
from core.forms import PostForm
from string import whitespace

isEmpty = lambda string: all(char in whitespace for char in str(string))

def home(request: HttpRequest):
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

def detail(request: HttpRequest, id: int):
    post = Post.objects.get(id=id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        comment = Comment(author=request.user, text=comment_text, post=post)
        comment.save()
        return redirect('core:detail', id=id)

    posts = [item for item in Post.objects.order_by('-id') if not item==post][:4]

    tags = Tag.objects.all()
    categories = Category.objects.all()

    context = {
        'post': post, 'tags': tags,
        'categories': categories, 'posts': posts
    }
    return render(request, 'single.html', context=context)

def about(request: HttpRequest):
    return render(request, 'about.html')

def extract_param(url: str, key: str):
    search = re.search(f"{key}=([^&]*)", url)
    if search:
        return search.group(1)

def stories(request: HttpRequest):
    # tag = extract_param(request.path, 'tag')
    # category = extract_param(request.path, 'category')
    print(request.GET)
    print([i for i in request.GET])
    tag = request.GET.get('tag')
    category = request.GET.get('category')
    if tag==None: tag='all'
    if category==None: category='all'
    if tag==category=="all":
        posts = Post.objects.order_by('-id')
    elif category!=tag=="all":
        posts = Post.objects.filter(category__title=category).order_by('-id')
    elif tag!=category=="all":
        posts = Post.objects.order_by('-id')
        posts = [post for post in posts if tag.title() in post.get_tags()]
    else:
        posts = Post.objects.filter(category__title=category).order_by('-id')
        posts = [post for post in posts if tag in post.get_tags()]

    POSTS = posts
    success = True
    search = request.GET.get('search')
    if isEmpty(search): search = None
    if search is not None:
        search = search.lower()
        posts = [post for post in POSTS if search in ' '.join((post.title, post.sub_title)).lower() or search in post.get_tags()]
        if not posts:
            success = False

    categories = Category.objects.all()
    context = {
        'posts': posts, 'categories': categories,
        'category': category, 'tag': tag,
        'search': search, 'success': success,
        'postcount': len(posts)
    }
    return render(request, 'stories.html', context=context)

def contact(request: HttpRequest):
    return render(request, 'contact.html')

def create_post(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('core:home')
    form = PostForm()
    return render(request, 'create_story.html', {'form': form})

# def search_view(request: HttpRequest):
#     POSTS = Post.objects.order_by('-id')
#     posts = POSTS
#     success = True
#     search = None
#     if request.method == 'POST':
#         search = str(request.POST.get('search')).lower()
#         if isEmpty(search): search = None
#         if search:
#             posts = [post for post in POSTS if search in ' '.join((post.title, post.sub_title)).lower() or search in post.get_tags()]
#             if not posts:
#                 success = False
#     context = {
#         'posts': posts, 'search': search,
#         'success': success, 'postcount': len(posts)
#     }
#     return render(request, 'search.html', context=context)

