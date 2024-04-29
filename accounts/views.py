from accounts.models import User
from core.models import *
from accounts.forms import *
from django.views.generic import *
from django.core.mail import *
from django.contrib.auth.views import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

# import random, string
# def generate_random_token() -> str:
#     return ''.join(random.sample(string.ascii_letters, 16))

def register(request: HttpRequest):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    form = RegisterForm()
    context = {
        'categories': categories, 'form': form
    }
    return render(request, 'register.html', context=context)

def login_auth(request: HttpRequest):
    categories = Category.objects.all()
    context = {'categories': categories}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:home')
    return render(request, 'login.html', context=context)

def profile(request: HttpRequest, id: int):
    user = User.objects.get(id=id)
    userposts = user.posts.order_by('-id')
    context = {
        "user": user, "userposts": userposts,
        'categories': Category.objects.all()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = Category.objects.all()
        return context

class ForgetPassword(PasswordResetView):
    form_class = ForgetPasswordForm
    template_name = 'forgot-password.html'
    success_url = reverse_lazy('accounts:login')
    email_template_name = "forgot-password-email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = Category.objects.all()
        return context

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name= "reset_password.html" 
    success_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = Category.objects.all()
        return context

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    form_class = ThePasswordChangeForm
    success_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = Category.objects.all()
        return context
