from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.utils import timezone
from django.views import View, generic

from .models import Article, Category

# Create your views here.


class IndexView(View):
    template_name = "wiki/index.html"
    # context_object_name = 'latest_question_list'

    def get(self, request):
        # with self make variable to class attribute, accessible to all methods
        # self.user_query = request.user
        # post_query = Post.objects.filter(page = 'events')
        category_query = Category.objects.all()
        if request.user.is_active:
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(visibility="public")
        articles_query = articles.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

        category_system = dict()
        for cat in category_query:
            category_system[cat] = articles.filter(category=cat)

        context = {
            "articles": articles_query,
            "categories": category_system,
            # 'user': self.user_query
        }

        return render(request, self.template_name, context)


class DetailView(UserPassesTestMixin, generic.DetailView):
    model = Article
    login_url = "/users/login/"
    template_name = "wiki/detail.html"

    def test_func(self):
        u = self.request.user
        a = Article.objects.get(slug=self.kwargs["slug"])
        if u.is_active:
            return True
        elif a.visibility == "public":
            return True
        else:
            return False

    def get(self, request, slug):
        # with self make variable to class attribute, accessible to all methods
        # self.user_query = request.user
        # post_query = Post.objects.filter(page = 'events')
        category_query = Category.objects.all()

        category_system = dict()
        for cat in category_query:
            category_system[cat] = Article.objects.filter(category=cat)

        article = Article.objects.get(slug=slug)

        context = {
            # 'posts':  post_query,
            "categories": category_system,
            "article": article,
        }

        return render(request, self.template_name, context)

    # def post(self, request):
