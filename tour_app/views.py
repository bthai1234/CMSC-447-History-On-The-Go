from django.shortcuts import get_object_or_404, render
from django.conf import settings

# Create your views here.
def index(request):
    context = {"google_api_key": settings.GOOGLE_API_KEY}#Retrieves the google api key from the setting.py file which in turn gets the key from the .env file 
    return render(request, 'tour_app/index.html', context)

def map_test(request):
    context = {"google_api_key": settings.GOOGLE_API_KEY}#Retrieves the google api key from the setting.py file which in turn gets the key from the .env file 
    return render(request, 'tour_app/map_test.html', context)