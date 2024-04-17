from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from django.contrib.auth import authenticate, login
from accounts.models import User

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:home')
    return render(request, 'login.html')

def profile(request, id):
    user = User.objects.get(id=id)
    myposts = user.posts.order_by('-id')
    context = {
        "user": user,
        "myposts": myposts
    }
    return render(request, 'user-profile.html', context=context)
