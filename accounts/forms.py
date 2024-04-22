from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        self.fields['first_name'].initial = self.instance.first_name
        self.fields['last_name'].initial = self.instance.last_name
        self.fields['bio'].initial = self.instance.bio
        self.fields['profile_pic'].initial = self.instance.profile_pic

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'profile_pic']

        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'placeholder': 'First Name*', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name', 'placeholder': 'Last Name*', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'id': 'bio', 'placeholder': 'Bio*', 'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'id': 'profile_pic', 'class': 'form-control'})
        }
