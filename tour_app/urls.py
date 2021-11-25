from django.urls import include, path
from . import views

app_name = 'tour_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='registerPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profilePage, name="profile"),
    path('tests/map_test', views.map_test, name='map_test'),
]