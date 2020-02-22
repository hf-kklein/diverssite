from django.urls import path

from django.contrib.auth import views

from users.views import Login

app_name = 'users'


urlpatterns = [
    path('login/', Login.as_view(), name = 'login'),
    path('password_reset/', views.PasswordResetView.as_view() , name = 'password_reset'),
    path('logout/', views.LogoutView.as_view(template_name= 'users/logout.html'), name = 'logout'),
    # path('register/', views.
]
