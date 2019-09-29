from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from .views import *
from rest_framework.routers import DefaultRouter


app_name = "users"

urlpatterns = [
    path('register/', UserListView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
