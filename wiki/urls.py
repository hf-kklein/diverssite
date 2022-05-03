from django.urls import path

from django.contrib.auth import views
from . import views

app_name = "wiki"


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<slug:slug>/", views.DetailView.as_view(), name="detail"),
]
