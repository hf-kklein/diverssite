"""diverssite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path("", include("public.urls")),
    path("polls/", include("polls.urls")),
    path("events/", include("events.urls")),
    path("admin/", admin.site.urls),
    # path('accounts/',include('django.contrib.auth.urls'), name = "accounts"),
    path("users/", include("users.urls")),
    path("wiki/", include("wiki.urls")),
    path("markdownx/", include("markdownx.urls")),
    path("mail/", include("mail.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
