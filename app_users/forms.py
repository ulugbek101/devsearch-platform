from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Skill, Profile, Message


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("*Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "off"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("*Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "off"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': '*Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
            'password1': '*Password',
            'password2': '*Password Confirmation',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input',
                'autocomplete': 'off',
            })


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'id', 'created', 'updated']
        labels = {
            'email': 'E-mail',
            'short_intro': 'Occupation',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input',
                'autocomplete': 'off',
                'autofocus': 'true'
            })


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input',
                'autofocus': 'true',
            })



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['fullname', 'email', 'subject', 'body']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input',
                'autofocus': 'true',
                'autocomplete': 'off',
                'required': 'true',
            })
        
