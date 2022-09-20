from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        widget=widgets.TextInput(
            attrs={
                'class': 'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800',
                'style': 'border: 1px solid #d3d5d8 !important',
                'placeholder': 'Username'
            }
        )
    )

    email = forms.EmailField(
        max_length=255,
        widget=widgets.TextInput(
            attrs={
                'class': 'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800',
                'style': 'border: 1px solid #d3d5d8 !important',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        max_length=255,
        widget=widgets.PasswordInput(
            attrs={
                'class': 'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800',
                'style': 'border: 1px solid #d3d5d8 !important',
                'placeholder': 'Password'
            }
        )
    )

    password2 = forms.CharField(
        max_length=255,
        widget=widgets.PasswordInput(
            attrs={
                'class': 'bg-gray-200 mb-2 shadow-none  dark:bg-gray-800',
                'style': 'border: 1px solid #d3d5d8 !important',
                'placeholder': 'Password Confirm'
            }
        )
    )

    def clean_username(self):
        value = self.cleaned_data['username']
        if get_user_model().objects.filter(username=self.cleaned_data['username']).exists():
            raise ValidationError(_('Username already exists!'))

        return value

    def clean_password2(self):
        password = self.cleaned_data['password']
        value = self.cleaned_data['password2']
        if password != value:
            raise ValidationError(_('Password not match!'))

        return value
