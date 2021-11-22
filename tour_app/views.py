from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, response

from tour_app.models import Itinerary
from .forms import RegisterUserForm
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from tour_app.models import Itinerary, Itinerary_location
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
def registerPage(request):
    regis_form = RegisterUserForm()
    context = {'regis_form': regis_form}
    # If I don't assign for var_password1 and var_password2, template would throw errors
    var_email = ""
    var_registered_email = "1"
    var_password1 = ""
    var_password2 = ""
    if request.method == 'POST':
        regis_form = RegisterUserForm(request.POST)
        var_email = request.POST['email']
        var_password1 = request.POST['password1']
        var_password2 = request.POST['password2']

        print("var_email = ", var_email)
        if regis_form.is_valid():
            emails = get_user_model().objects.all()
            for objectName in emails:
                print(objectName.email)
                if var_email == objectName.email:
                    messages.error(request, "Email has been used")
                    messages.info(request,
                                  "Notes: User would be redirect to registration page if they provide invalid information")
                    return render(request, 'tour_app/registration.html', context)

            regis_form.save()
            var_username = request.POST['username']
            user = get_user_model().objects.get(username=var_username)
            new_itinerary = Itinerary(user_id=user.id, itinerary_name=(var_username + ' Itinerary'))
            new_itinerary.save()
            return HttpResponseRedirect(reverse('tour_app:loginPage'))

    # if var_email == var_registered_email:
    #     # var_is_email_existing = True
    #     messages.error(request, "Email has been used")
    # else:
    #     print("Email")
    if var_password1 == var_password2:
        print("Password Matched")
    else:
        messages.error(request, "Password is not matching")

    messages.info(request, "Notes: User would be redirect to registration page if they provide invalid information")
    return render(request, 'tour_app/registration.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('tour_app:mapPage'))

    context = {}
    return render(request, 'tour_app/login.html', context)


def index(request):
    context = {
        "google_api_key": settings.GOOGLE_API_KEY}  # Retrieves the google api key from the setting.py file which in turn gets the key from the ..env file
    return render(request, 'tour_app/index.html', context)


def mapPage(request):
    context = {
        "google_api_key": settings.GOOGLE_API_KEY}  # Retrieves the google api key from the setting.py file which in turn gets the key from the ..env file
    return render(request, 'tour_app/mapPage.html', context)


def map_test(request):
    context = {
        "google_api_key": settings.GOOGLE_API_KEY}  # Retrieves the google api key from the setting.py file which in turn gets the key from the ..env file
    return render(request, 'tour_app/map_test.html', context)


def saveLocation(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user.username
        Itinerary_obj = Itinerary.objects.get(itinerary_name=user + " Itinerary")

        location_name = request.POST['place_name']
        lat = request.POST['lat']
        long = request.POST['lng']
        location = Itinerary_location(loc_name=location_name, latitude=lat, longitude=long,
                                      itinerary_id=Itinerary_obj.id)
        location.save()
        response = JsonResponse({"message": "Location added to Itinerary"})
        response.status_code = 201
        return response  # Sending an success response
    else:
        response = JsonResponse({"message": "Can not save location to initnerary, user not logged in."})
        response.status_code = 200
        return response
