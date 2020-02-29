from django.shortcuts import render
from django.views import generic, View
from .models import Category, Articles
from public.models import Post
from django.utils import timezone
# Create your views here.

class IndexView(View):
    template_name = 'wiki/index.html'
    # context_object_name = 'latest_question_list'

    def get(self, request):
        # with self make variable to class attribute, accessible to all methods
        # self.user_query = request.user
        # post_query = Post.objects.filter(page = 'events')
        category_query = Category.objects.all()
        articles_query = Articles.objects.filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

        category_system = dict()
        for cat in category_query:
            category_system[cat] = Articles.objects.filter(category=cat)

        context = {
                   'articles':  articles_query,
                   'categories': category_system,
                   # 'user': self.user_query
                   }

        return render(request, self.template_name, context)



class DetailView(generic.DetailView):
    model = Articles
    template_name = 'wiki/detail.html'

    def get(self, request, slug):
        # with self make variable to class attribute, accessible to all methods
        # self.user_query = request.user
        # post_query = Post.objects.filter(page = 'events')
        category_query = Category.objects.all()

        category_system = dict()
        for cat in category_query:
            category_system[cat] = Articles.objects.filter(category=cat)

        article = Articles.objects.get(slug=slug)

        context = {
                   # 'posts':  post_query,
                   'categories': category_system,
                   'article': article
                   }

        return render(request, self.template_name, context)

    # def post(self, request):
