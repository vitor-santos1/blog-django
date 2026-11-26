from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {"content": forms.Textarea(attrs={"rows": 10})}


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username",)
