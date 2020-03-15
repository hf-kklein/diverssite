from django.urls import path
from django.views.generic import View
from django.contrib.auth import views

from users.views import Login, SignUp, RegComplete

app_name = 'users'


urlpatterns = [
    path('login/', Login.as_view(), name = 'login'),
    path('password_reset/', views.PasswordResetView.as_view() , name = 'password_reset'),
    path('logout/', views.LogoutView.as_view(template_name= 'users/logout.html'), name = 'logout'),
    path('signup/', SignUp.as_view(template_name='users/signup.html'), name='signup'),
    path('thanks/', RegComplete.as_view(), name = 'thanks')
]
