from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterUserForm
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, 'tour_app/index.html', context={})


def registerPage(request):
    regis_form = RegisterUserForm()
    context = {'regis_form': regis_form}
    if request.method == 'POST':
        regis_form = RegisterUserForm(request.POST)
        if regis_form.is_valid():
            regis_form.save()
            return HttpResponseRedirect(reverse('tour_app:loginPage'))
    return render(request, 'tour_app/registerPage.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('tour_app:index'))

    context = {}
    return render(request, 'tour_app/loginPage.html', context)


def regis_success(request):
    context = {}
    return render(request, 'tour_app/regis_success.html', context)
