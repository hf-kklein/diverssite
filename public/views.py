from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from wiki.models import Articles, Display


class IndexView(generic.ListView):
    model = Articles
    template_name = 'public/home.html'
    context_object_name = 'home_public_posts'

    def get_context_data(self, **kwargs):
        welcome_title = "Saxy Divers Ultimate Frisbee"
        welcome_text = "Saxy Divers spielen seit 1990 Ultimate Frisbee in Leipzig"
        home = Display.objects.get(name = 'home')
        posts = Articles.objects.filter(show_on_pages = home)
        public_posts = posts.filter(visibility = 'public')
        published_posts = public_posts.filter(pub_date__lte=timezone.now())
        published_posts

        context = { 'welcome_title': welcome_title,
                    'welcome_text': welcome_text,
                    'published_posts': published_posts
                    }
        return context
