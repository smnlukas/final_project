from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget
from .models import Category
from django.forms import widgets

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'website', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.HiddenInput(),
            'content': CKEditorWidget(),
            'website': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.HiddenInput(attrs={'value': 0}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['author'].disabled = True
        self.fields['author'].initial = user