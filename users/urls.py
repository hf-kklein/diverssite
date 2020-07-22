from django.urls import path
from django.views.generic import View
from django.contrib.auth import views

from users.views import Login, SignUpView, RegComplete, ProfileView

app_name = 'users'


urlpatterns = [
    path('login/', Login.as_view(), name = 'login'),
    path('password_reset/', views.PasswordResetView.as_view() , name = 'password_reset'),
    path('logout/', views.LogoutView.as_view(template_name= 'users/logout.html'), name = 'logout'),
    path('signup/', SignUpView.as_view(template_name='users/signup.html'), name='signup'),
    path('thanks/', RegComplete.as_view(), name = 'thanks'),
    path('<str:username>/', ProfileView.as_view(), name = 'profile'),
    path('change-password/', views.PasswordChangeView.as_view(template_name='commons/change-password.html'), name='change_password'),
]
