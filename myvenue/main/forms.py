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


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'inputFullName',
            'placeholder': 'Full Name'
        }))

    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'id': 'inputEmail',
            'placeholder': 'Email Address'
        }))

    phone_number = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'id': 'inputPhoneNumber',
            'placeholder': 'Phone Number'
        }))

    address = forms.CharField(max_length=200, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'inputAddress',
            'placeholder': 'Address'
        }))


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
