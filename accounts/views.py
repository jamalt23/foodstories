from django.shortcuts import render, redirect
from accounts.forms import *
from django.contrib.auth import authenticate, login
from accounts.models import User
from django.http import HttpRequest
from django.views.generic import *
from django.contrib.auth.views import *
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.core.mail import *
import random, string

# def generate_random_token() -> str:
#     return ''.join(random.sample(string.ascii_letters, 16))

def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_auth(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:home')
    return render(request, 'login.html')

def profile(request: HttpRequest, id: int):
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


class ForgetPassword(PasswordResetView):
    form_class = ForgetPasswordForm
    template_name = 'forgot-password.html'
    success_url = reverse_lazy('accounts:login')
    email_template_name = "forgot-password-email.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name= "reset_password.html" 
    success_url = reverse_lazy('accounts:login')
    form_class = PasswordResetConfirmForm

# def forgot_password(request: HttpRequest):
#     success = None
#     if request.method == 'POST':
#         userdata = request.POST.get('userdata')
#         user = [user for user in User.objects.filter(username=userdata)]
#         if user == []:
#             user == [user for user in User.objects.filter(email=userdata)]
#         if user:
#             user = user[0]
#             success = True
#             EmailMessage('Password reset',
#                     'Password reset link: https://www.localhost:8000/accounts/reset-password/'+user.username,
#                     'foodstories657@gmail.com',
#                     [user.email]).send()

#         else:
#             success = False
#             return render(request, 'forgot-password.html', {'success':success})
#     return render(request, 'forgot-password.html', {'success':success})

# def success_password_request(request: HttpRequest):
#     return render(request, 'success-password-request.html')
