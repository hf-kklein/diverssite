from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views

from users.views import Login, SignUpView, RegComplete, ProfileView

app_name = 'users'


urlpatterns = [
    path('login/', Login.as_view(), name = 'login'),
    path('password_reset/', views.PasswordResetView.as_view(), name = 'password_reset'),
    path('logout/', views.LogoutView.as_view(template_name= 'users/logout.html'), name = 'logout'),
    path('signup/', SignUpView.as_view(template_name='users/signup.html'), name='signup'),
    path('thanks/', RegComplete.as_view(), name = 'thanks'),
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('change-password/', views.PasswordChangeView.as_view(success_url=reverse_lazy('users:password_change_done')), name='change_password'),
    path('password_change_done/', views.PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name='password_change_done'),

]
