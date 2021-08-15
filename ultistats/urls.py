from django.urls import path

from . import views

app_name = 'ultistats'

urlpatterns = [
    path('', views.StatsFormView.as_view(), name="ultistats"),
]
