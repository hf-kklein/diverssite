from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


# Create your views here.

# def index(request):
#     welcome_text = "Welcome to the Website of the Saxy Divers"
#     return HttpResponse(welcome_text)

def index(request):
    # print(request)
    welcome_text = "Welcome to the Website of the Saxy Divers"
    context = {'welchome_text':welcome_text}
    return render(request, 'public/index.html', context)
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
