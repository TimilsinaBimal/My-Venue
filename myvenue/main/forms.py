from django import forms
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.models import User


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):

        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.error_css_class = 'is_invalid'
        self.fields['remember'].widget.attrs.update({
            'class': 'custom-control-input',
            'id': 'customCheck1'
        })
        self.fields['login'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inputEmail',
            'placeholder': 'Email address'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inputPassword',
            'placeholder': 'Password'
        })


class SignUpForm(SignupForm):
    first_name = forms.CharField(max_length=30,  required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'inputfirstName',
            'placeholder': 'First Name'
        }))

    last_name = forms.CharField(
        max_length=30, label='Last Name', required=True, widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'inputlastName',
                'placeholder': 'Last Name'
            }))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.error_css_class = 'is_invalid'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inputUsername',
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inputEmail',
            'placeholder': 'Email Address'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inputPassword',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inputConfirmPassword',
            'placeholder': 'Confirm Password'
        })
