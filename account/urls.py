from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path("login/", auth_views.LoginView.as_view()),
]
