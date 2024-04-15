from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'placeholder' : 'Password*',
                'class' : 'form-control',
            }))

    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'placeholder' : 'Confirm password*',
                'class' : 'form-control',
             }))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'password1', 'password2','profile_pic']

        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'placeholder': 'First Name*', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name', 'placeholder': 'Last Name*', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'id': 'username', 'placeholder': 'Username*', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Email*', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'id': 'bio', 'placeholder': 'Bio*', 'class': 'form-control'}),
        }


# class LoginForm(forms.Form):
#     username = forms.CharField(
#         widget = forms.TextInput(
#             attrs={
#                 'placeholder' : 'Username*',
#                 'class' : 'form-control',
#             }))
#     password = forms.CharField(
#         widget = forms.PasswordInput(
#             attrs={
#                 'placeholder' : 'Password*',
#                 'class' : 'form-control',
#             }))