from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, 'tour_app/index.html', context={})


def registerPage(request):
    regis_form = RegisterUserForm();
    if request.method == 'POST':
        regis_form = RegisterUserForm(request.POST)
        if regis_form.is_valid():
            regis_form.save()
    return render(request, 'tour_app/registerPage.html', context={'regis_form': regis_form})


def loginPage(request):
    return render(request, 'tour_app/loginPage.html', context={})
