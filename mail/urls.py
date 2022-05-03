from django.urls import path

from . import views

app_name = "mail"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("compose/", views.ComposeView.as_view(), name="compose"),
]
