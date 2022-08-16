from django import forms
from .import models

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CreateInterviewDatabase(forms.ModelForm):
    class Meta:
        model=models.InterviewDatabase
        fields=['date','year','cname','branch','title','interexp','file']



class CreateResourceDatabase(forms.ModelForm):
    class Meta:
        model=models.ResourceDatabase
        fields=['date','sname','topic','resourceDesc','file']







class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'branch', 'company_name', 'yoj', 'linkedIn']



