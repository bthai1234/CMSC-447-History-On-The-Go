from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets

from tour_app.models import Profile


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, label="First Name",
                                 widget=forms.TextInput(attrs={
                                     "placeholder": "Enter First Name",
                                     "class": "form-input"}))
    last_name = forms.CharField(max_length=255, label="Last Name",
                                widget=forms.TextInput(attrs={
                                    "placeholder": "Enter Last Name",
                                    "class": "form-input"}))
    email = forms.EmailField(max_length=255, label="Email Address",
                             widget=forms.TextInput(attrs={
                                 "placeholder": "example@email.com",
                                 "class": "form-input"}))
    city = forms.CharField(max_length=255, label="City",
                           widget=forms.TextInput(attrs={
                               "placeholder": "Enter City",
                               "class": "form-input"}))
    address = forms.CharField(max_length=255, label="Home Address",
                              widget=forms.TextInput(attrs={
                                  "placeholder": "Enter Home Address",
                                  "class": "form-input"}))
    zipcode = forms.CharField(max_length=5, label="Zip Code",
                              widget=forms.TextInput(attrs={
                                  "placeholder": "00000",
                                  "class": "form-input"}))

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


def form_validation_check(form) -> str:
    """If any error occurs in the form, return an error message

    param form: the form that is passed in
    returns: error message for the associated form field
    """
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field.label,
                                   'label') else 'Error', error)
    return msg
