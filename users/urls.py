from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views

from users.views import Login, SignUpView, RegComplete, ProfileView, AccountActivateView

app_name = 'users'


urlpatterns = [
    path('login/', Login.as_view(), name = 'login'),
    path('logout/', views.LogoutView.as_view(
        template_name= 'users/logout.html'
        ), name = 'logout'),
    
    path('password_reset/', views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_mail.html',
        success_url=reverse_lazy('users:password_reset_done')
        ), name = 'password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html"
        ), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
        success_url=reverse_lazy('users:password_reset_complete')
        ), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html"
        ), name='password_reset_complete'),
        
    
    path('signup/', SignUpView.as_view(template_name='users/signup.html'), name='signup'),
    # path('activate/', AccountActivateView.as_view(template_name='account_activation.html'), name = 'activate'),
    path('thanks/', RegComplete.as_view(), name = 'thanks'),
    
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('change-password/', views.PasswordChangeView.as_view(
        success_url=reverse_lazy('users:password_change_done')
        ), name='change_password'),
    path('password_change_done/', views.PasswordChangeDoneView.as_view(
        template_name="users/password_change_done.html"
        ), name='password_change_done'),
]
