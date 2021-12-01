from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


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