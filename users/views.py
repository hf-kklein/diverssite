from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class Login(LoginView):
    template_name = "users/login.html"


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'signup.html'
