from django import forms
from django.contrib.auth.models import User
from posts.models import Post, Comment
from django.utils.safestring import mark_safe
from django.forms.widgets import FileInput, CheckboxInput
from django.utils.html import format_html
from django.utils.encoding import force_text

# source: http://stackoverflow.com/questions/17293627/hide-django-clearablefileinput-checkbox
class NotClearableFileInput(FileInput):

    template_with_initial = '%(initial_text)s: %(initial)s <br />%(clear_text)s: %(clear)s<br />%(input_text)s: %(input)s<br />'

    url_markup_template = '<br/><img src="/static/{0}" height="100" width="100"/>'

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': "Current File",
            'clear_text': "Remove Current Image",
            'input_text': "Change",

        }
        template = '%(input)s'
        substitutions['input'] = super(NotClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = format_html(self.url_markup_template,
                                               value.url,
                                               force_text(value))
            substitutions['clear'] = CheckboxInput().render("clear", False, attrs={'id': 'clear'})

        return mark_safe(template % substitutions)

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=("post_text","title","privacy","allowed","description", "image", "content_type")
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PostForm, self).__init__(*args, **kwargs)
        #Excludes the username of the current user and admin from the list of possible users
        #that can be choosen for a post to be custom to
        #self.fields["allowed"].queryset = User.objects.exclude(username="admin").exclude(username=user)
        
        
        #make the forms better 
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['content_type'].widget.attrs['class'] = 'form-control'
        self.fields['post_text'].widget.attrs['class'] = 'form-control'
        self.fields['privacy'].widget.attrs['class'] = 'form-control'        

class EditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=("post_text","title","privacy","allowed","description","image", "content_type")
        widgets = {
             'image':NotClearableFileInput()
        }
    def __init__(self, user, post,*args, **kwargs):
        self.post=post
        self.user = user
        super(EditForm, self).__init__(*args, **kwargs)
        #Initializes all the fields with the existing posts information
        #self.fields["allowed"].queryset = User.objects.exclude(username="admin").exclude(username=user)
        self.fields["title"].initial=post.title
        self.fields["description"].initial=post.description
        self.fields["content_type"].initial=post.content_type
        self.fields["post_text"].initial=post.post_text
        self.fields["privacy"].initial=post.privacy
        self.fields["image"].initial=post.image
        #if post.privacy=="3":
         #   self.fields["allowed"].initial=[t.pk for t in post.allowed.all()]
        
        #make the forms better  
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['content_type'].widget.attrs['class'] = 'form-control'
        self.fields['post_text'].widget.attrs['class'] = 'form-control'
        self.fields['privacy'].widget.attrs['class'] = 'form-control'
       

class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ("body",)
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs) 
        self.fields['body'].widget.attrs['class'] = 'form-control'    
