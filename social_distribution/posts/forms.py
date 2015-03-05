from django import forms
from django.contrib.auth.models import User
from posts.models import Post
from django.forms.widgets import CheckboxSelectMultiple 

class PostForm(forms.ModelForm):
    #allowed = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model=Post
        fields=("post_text","title","privacy","allowed")
    def __init__(self, user, *args, **kwargs):  
        self.user = user
        super(PostForm, self).__init__(*args, **kwargs) 
        self.fields["allowed"].queryset = User.objects.exclude(username="admin").exclude(username=user)    
