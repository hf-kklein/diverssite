from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Post


class IndexView(generic.ListView):
    model = Post
    template_name = 'public/home.html'
    context_object_name = 'home_public_posts'

    def get_context_data(self, **kwargs):
        welcome_title = "Saxy Divers Ultimate Frisbee"
        welcome_text = "Saxy Divers spielen seit 1990 Ultimate Frisbee in Leipzig"
        public_posts = Post.objects.filter(visibility = 'public')
        published_posts = public_posts.filter(pub_date__lte=timezone.now())
        queryset = published_posts

        context = { 'welcome_title': welcome_title,
                    'welcome_text': welcome_text,
                    'published_posts': published_posts
                    }
        return context
