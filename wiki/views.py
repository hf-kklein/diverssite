import os
from django.http.response import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View, generic
from django.contrib.auth.decorators import login_required

from .models import Article, Category, Image, File
from . import models


def get_articles_for_user(user):
    if user.is_active:
        return Article.objects.all()
    else:
        return Article.objects.filter(visibility="public")


def nest_articles_in_categories(articles):
    categories = Category.objects.all()
    category_system = dict()
    for cat in categories:
        category_system[cat] = articles.filter(category=cat)

    return category_system


class IndexView(View):
    template_name = "wiki/index.html"

    def get(self, request):
        articles = get_articles_for_user(user=request.user)
        category_system = nest_articles_in_categories(articles=articles)

        articles_query = articles.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

        context = {
            "articles": articles_query,
            "categories": category_system,
        }

        return render(request, self.template_name, context)


@login_required
def secure(request, file):
    if "image" in file:
        model = Image
    elif "file" in file:
        model = File
    else:
        raise NotImplementedError

    file = get_object_or_404(model, file=f"private/wiki/{file}")
    response = FileResponse(file.file)
    return response


class DetailView(UserPassesTestMixin, generic.DetailView):
    model = Article
    login_url = "/users/login/"
    template_name = "wiki/detail.html"

    def test_func(self):
        """
        test function for class UserPassesTestMixin to regulate access to
        article
        """
        u = self.request.user
        a = Article.objects.get(slug=self.kwargs["slug"])
        if u.is_active:
            return True
        elif a.visibility == "public":
            return True
        else:
            return False

    def get(self, request, slug):
        articles = get_articles_for_user(user=request.user)
        category_system = nest_articles_in_categories(articles=articles)

        article = Article.objects.get(slug=slug)

        context = {
            "categories": category_system,
            "article": article,
        }

        return render(request, self.template_name, context)
