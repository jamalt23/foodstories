from django.shortcuts import render, redirect
from accounts.forms import *
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

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if not request.FILES.get('profile_pic'):
                form
            if not request.POST.get('bio'):
                form.cleaned_data.pop('bio')
            if not request.POST.get('first_name'):
                form.cleaned_data.pop('first_name')
            if not request.POST.get('last_name'):
                form.cleaned_data.pop('last_name')
            
            form.save()
            return redirect(f'accounts:profile', id=request.user.id)
    form = EditProfileForm()
    return render(request, 'edit-profile.html', {'form': form})
