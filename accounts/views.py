from accounts.models import User
from core.models import *
from accounts.forms import *
from django.views.generic import *
from django.core.mail import *
from django.contrib.auth.views import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import *
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.db.models.query import QuerySet

def register(request: HttpRequest):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.is_active = False
            user = form.save()
            domain = get_current_site(request).domain
            email_subject = "Activate your account"
            message = render_to_string('activate-email.html', {
                'user': user, 'domain': domain,
                'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user), 
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            context = {'categories': categories, 'sent_email' : True}
            return render(request, 'login.html', context=context)

    form = RegisterForm()
    context = {
        'categories': categories, 'form': form
    }
    return render(request, 'register.html', context=context)

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('core:home')
    else:
        return HttpResponse('Activation link is invalid!')

def login_auth(request: HttpRequest):
    categories = Category.objects.all()
    context = {'categories': categories, 'sent_email' : False}
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
    userposts: QuerySet[Post] = user.posts.order_by('-id')
    success = True
    search = request.GET.get('search')
    if isEmpty(search) or search == "None": search = None
    if search is not None:
        search = search.lower()
        userposts: QuerySet[Post] = [post for post in userposts if search in ' '.join((post.title, post.sub_title)).lower() or search in post.get_tags(case='lower')]
        if not userposts:
            success = False
    context = {
        "user": user, "userposts": userposts,
        "success": success, "search": search,
        "categories": Category.objects.all()
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
