from django.contrib.auth import views
from django.urls import path

from . import views

app_name = "wiki"


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<slug:slug>/", views.DetailView.as_view(), name="detail"),
]
