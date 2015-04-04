from django import forms
from django.contrib.auth.models import User
from authors.models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('displayname', 'body', 'birthdate', 'gender', 'github', 'workspace', 'school')
        widgets = {
            'birthdate': forms.TextInput(attrs={'placeholder':'yyyy-mm-dd'})
        }
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs) 
        self.fields['displayname'].widget.attrs['class'] = 'form-control'
        self.fields['body'].widget.attrs['class'] = 'form-control'
        self.fields['birthdate'].widget.attrs['class'] = 'form-control'
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['github'].widget.attrs['class'] = 'form-control' 
        self.fields['workspace'].widget.attrs['class'] = 'form-control'        
        self.fields['school'].widget.attrs['class'] = 'form-control'        