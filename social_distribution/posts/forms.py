from django import forms
from django.contrib.auth.models import User
from posts.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=("post_text","title","privacy","allowed","description")
    def __init__(self, user, *args, **kwargs):  
        self.user = user
        super(PostForm, self).__init__(*args, **kwargs) 
        #Excludes the username of the current user and admin from the list of possible users
        #that can be choosen for a post to be custom to
        self.fields["allowed"].queryset = User.objects.exclude(username="admin").exclude(username=user)
        self.fields['title'].length = 128

class EditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=("post_text","title","privacy","allowed","description")
    def __init__(self, user, post,*args, **kwargs):  
        self.post=post
        self.user = user
        super(EditForm, self).__init__(*args, **kwargs)  
        #Initializes all the fields with the existing posts information
        self.fields["allowed"].queryset = User.objects.exclude(username="admin").exclude(username=user)
        self.fields["title"].initial=post.title
        self.fields["description"].initial=post.description
        self.fields["post_text"].initial=post.post_text
        self.fields["privacy"].initial=post.privacy
        if post.privacy=="3":
            self.fields["allowed"].initial=[t.pk for t in post.allowed.all()]
       
class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ("body",)