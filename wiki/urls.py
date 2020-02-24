from django.urls import path

from django.contrib.auth import views

app_name = 'wiki'


urlpatterns = [
    path('/', Wiki.as_view(), name = 'wiki'),
]
