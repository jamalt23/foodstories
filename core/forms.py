from django import forms
from core.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'sub_title', 'image', 'text', 'category', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'sub_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sub Title'}),
            'image': forms.FileInput(attrs={'class': 'form-contrsdsol', 'placeholder': 'Image'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Text'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-conrol'}),
        }
    