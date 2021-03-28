from django import forms
from .models import userInfo
from django.contrib.auth.models import User


class userForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password']


class userInfoForm(forms.ModelForm):
    class Meta():
        model = userInfo
        fields = ['mobile_number', 'proof_of_user']
