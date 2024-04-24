from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from string import whitespace

isEmpty = lambda string: all(char in whitespace for char in str(string))

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

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'profile_pic']

        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'placeholder': 'First Name*', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name', 'placeholder': 'Last Name*', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'id': 'bio', 'placeholder': 'Bio*', 'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'id': 'profile_pic', 'class': 'form-control'})
        }

class ForgetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        widget = forms.EmailInput(attrs={
            'placeholder': 'Your Email',
            'class': 'form-control',
        })
    )

class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'placeholder' : 'New password',
                'class' : 'form-control',
             }))
    
    new_password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'placeholder' : 'Re-enter new password',
                'class' : 'form-control',
             }))

    class Meta:
        fields = ("new_password1", 'new_password2', )