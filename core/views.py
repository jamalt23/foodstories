import re, json
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import *
from core.models import *
from django.views.generic import *
from django.core.exceptions import PermissionDenied
from core.forms import PostForm
from django.urls import reverse_lazy
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
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'usercount': User.objects.count(),
        'postcount': Post.objects.count()
    }
    return render(request, 'about.html', context=context)

def extract_param(url: str, key: str):
    search = re.search(f"{key}=([^&]*)", url)
    if search:
        return search.group(1)

def stories(request: HttpRequest):
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
    if isEmpty(search) or search == "None": search = None
    if search is not None:
        search = search.lower()
        posts = [post for post in POSTS if search in ' '.join((post.title, post.sub_title)).lower() or search in post.get_tags(case='lower')]
        if not posts:
            success = False

    categories = Category.objects.all()
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'posts': posts, 'categories': categories,
        'category': category, 'tag': tag,
        'search': search, 'success': success,
        'postcount': len(posts), 'page': page,
        'tags': Tag.objects.all()
    }
    return render(request, 'stories.html', context=context)

def contact(request: HttpRequest):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'contact.html', context=context)

class CreatePost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_story.html'
    success_url = reverse_lazy('core:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super(CreatePost, self).dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('core:home')

class EditPost(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'create_story.html'

    def get_success_url(self):
        return reverse_lazy('core:detail', kwargs={'id':self.get_object().id})
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            raise PermissionDenied
        return super(EditPost, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = Category.objects.all()
        return context