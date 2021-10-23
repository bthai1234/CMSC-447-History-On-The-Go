from django.urls import include, path

from . import views

app_name = 'tour_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='registerPage'),
    path('login/', views.loginPage, name='loginPage'),
]
