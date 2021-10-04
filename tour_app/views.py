from django.shortcuts import get_object_or_404, render

# Create your views here.
def index(request):
    return render(request, 'tour_app/index.html', context={})