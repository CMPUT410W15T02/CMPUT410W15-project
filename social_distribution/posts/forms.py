from django import forms
from django.contrib.auth.models import User
from posts.models import Post

class PostForm(forms.ModelForm):
    #allowed = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model=Post
        fields=("post_text","title","privacy","allowed")
        
