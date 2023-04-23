from django.contrib.auth.forms import PasswordChangeForm
from socket import fromshare
from django import forms
from django.forms import ModelForm
from .models import ChatMessage, Profile


class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={"class": "forms", "rows": 3, "placeholder": "Type message here"}))

    class Meta:
        model = ChatMessage
        fields = ["body", ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pic']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old password'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}))
