from django import forms
from django.contrib.auth.models import User
from authors.models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('body', 'birthdate', 'gender', 'image', 'workspace', 'school')
