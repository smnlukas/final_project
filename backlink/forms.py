from django import forms
from .models import Post, User, ArticleOrder
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserChangeForm


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


class ArticleOrderForm(forms.ModelForm):
    payment = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = ArticleOrder
        fields = ['f_name', 'l_name', 'bank_account_number', 'product', 'payment']


class UserProfileUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = User
        fields = ['username', 'email', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }


