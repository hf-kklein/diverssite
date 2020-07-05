from django.shortcuts import render
from django.views import View, generic
from .models import Message
from .forms import ComposeForm

# Create your views here.



class IndexView(generic.ListView):
    template_name = 'mail/index.html'
    context_object_name = 'sent_mails'

    def get_queryset(self):
        """
        Show all sent emails
        """
        return Message.objects.all()
            # .order_by('-time')


class DetailView(generic.DetailView):
    model = Message
    template_name = 'mail/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Message.objects.all()



class ComposeView(generic.FormView):
    template_name = 'mail/compose.html'
    form_class = ComposeForm
    success_url = '/thanks/'
