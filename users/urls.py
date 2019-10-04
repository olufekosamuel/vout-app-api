from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from .views import *
from rest_framework.routers import DefaultRouter


app_name = "users"

urlpatterns = [
    path('register/', csrf_exempt(UserListView.as_view()), name="register"),
    #path('signup2/',RegistrationForExistingChannel, name='signup2'),
    path('signup/',Registration, name='signup'),
    path('login/', csrf_exempt(LoginView.as_view()), name="login"),
    path('logout/', csrf_exempt(LogoutView.as_view()), name="logout"),
]
