from django.shortcuts import get_object_or_404, render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
<<<<<<< HEAD
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, response
from django.contrib.auth.decorators import login_required
from tour_app.models import Itinerary
from .forms import RegisterUserForm
=======
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterUserForm, ProfileForm, form_validation_check
>>>>>>> 1ec7c79 (Created ProfileForm and parts of profileView)
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from tour_app.models import Itinerary, Itinerary_location
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError

app_name = 'main'

# Create your views here.
def registerPage(request):
    regis_form = RegisterUserForm()
    context = {'regis_form': regis_form}
    # If I don't assign for var_password1 and var_password2, template would throw errors
    var_email = ""
    var_registering_username = ""
    var_password1 = ""
    var_password2 = ""
    if request.method == 'POST':
        regis_form = RegisterUserForm(request.POST)
        var_registering_username = request.POST['username']
        var_email = request.POST['email']
        var_password1 = request.POST['password1']
        var_password2 = request.POST['password2']

        print("var_email = ", var_email)
        try:
            if get_user_model().objects.get(username=var_registering_username):
                messages.error(request, "Username has been used")
                messages.info(request, "Notes: Invalid information would cause a redirection to this page")
                return render(request, 'tour_app/registration.html', context)
        except:
            print("Good for register")

        if regis_form.is_valid():
            emails = get_user_model().objects.all()
            if any(True for objectName in emails if var_email == objectName.email):
                messages.error(request, "Email has been used")
                messages.info(request, "Notes: Invalid information would cause a redirection to this page")
                return render(request, 'tour_app/registration.html', context)

            # for objectName in emails:
            #     print(objectName.email)
            #     if var_email == objectName.email:
            #         messages.error(request, "Email has been used")
            #         messages.info(request,
            #                       "Notes: User would be redirect to registration page if username has been used")
            #         return render(request, 'tour_app/registration.html', context)
            regis_form.save()
            var_username = request.POST['username']
            user = get_user_model().objects.get(username=var_username)
            new_itinerary = Itinerary(user_id=user.id, itinerary_name=(var_username + ' Itinerary'))
            new_itinerary.save()
            return HttpResponseRedirect(reverse('tour_app:loginPage'))

    if var_password1 == var_password2:
        print("Password Matched")
    else:
        messages.error(request, "Password is not matching")

    messages.info(request, "Notes: Invalid information would cause a redirection to this page")
    return render(request, 'tour_app/registration.html', context)


def loginPage(request):
    var_flag = False
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == "":
            var_flag = True
            messages.error(request, "Please provide username")
        if password == "":
            var_flag = True
            messages.error(request, "Please provide password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('tour_app:mapPage'))
        else:
            if not var_flag:
                try:
                    if get_user_model().objects.get(username=username):
                        messages.error(request, "Incorrect Password")
                        return render(request, 'tour_app/login.html', context)
                except:
                    print("Cannot find reason")

                messages.error(request, "Cannot find username")
                return render(request, 'tour_app/login.html', context)

    return render(request, 'tour_app/login.html', context)


# user profile form page
@login_required(login_url=' tour_app/login/')
def profilePage(request):
    return render(request, 'tour_app/profilePage.html', {})



def profilePage(request):
    pass


def index(request):
    context = {
        "google_api_key": settings.GOOGLE_API_KEY}  # Retrieves the google api key from the setting.py file which in turn gets the key from the ..env file
    return render(request, 'tour_app/index.html', context)


<<<<<<< HEAD

def mapPage(request):
    if request.method == 'POST':
        context = {
            "figure": request.POST['figure'],
            "lat": request.POST['lat'],
            "lng": request.POST['lng'],
            "placeName": request.POST['placeName'],
            "radius": request.POST['radius'],
            "google_api_key": settings.GOOGLE_API_KEY
            }
    else:    
        context = {"google_api_key": settings.GOOGLE_API_KEY}  # Retrieves the google api key from the setting.py file which in turn gets the key from the ..env file
    
    return render(request, 'tour_app/mapPage.html', context)



=======
>>>>>>> 1ec7c79 (Created ProfileForm and parts of profileView)
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
        response.status_code = 403  
        return response

def logout_request(request):
    logout(request)
    messages.info(request, "You have logged out")
    return redirect("tour_app:mapPage")
