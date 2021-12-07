from django.urls import include, path
from . import views

app_name = 'tour_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.mapPage, name='mapPage'),
    path('register/', views.registerPage, name='registerPage'),
    path('login/', views.loginPage, name='loginPage'),
<<<<<<< HEAD
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profilePage, name="profile"),
=======
    path('profile/', views.profilePage, name="profielPage"),
>>>>>>> 1ec7c79 (Created ProfileForm and parts of profileView)
    path('tests/map_test', views.map_test, name='map_test'),
    path('saveLocation/', views.saveLocation, name='saveLocation'),
]
