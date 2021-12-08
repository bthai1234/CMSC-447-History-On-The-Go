from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from tour_app.models import UserLocation


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    class Meta:
        model = UserLocation
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
            msg += "%s: %s \\n" % (field.label if hasattr(field.label, 'label') else 'Error', error) 
    return msg