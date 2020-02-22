from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView, PasswordResetView


class Login(LoginView):
    template_name = "users/login.html"
