from django.shortcuts import render, redirect
from accounts.forms import *
from django.contrib.auth import authenticate, login
from accounts.models import User
from django.http import HttpRequest
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

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
    userposts = user.posts.order_by('-id')
    context = {
        "user": user,
        "userposts": userposts
    }
    return render(request, 'user-profile.html', context=context)


class EditProfile(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'edit-profile.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'id':self.get_object().id})
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.username != self.get_object().username:
            raise PermissionDenied
        return super(EditProfile, self).dispatch(request, *args, **kwargs)

