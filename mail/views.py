from django.shortcuts import render
from django.views import View, generic
from .models import Message
from .forms import ComposeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
# Create your views here.



class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/users/login/'
    template_name = 'mail/index.html'
    context_object_name = 'sent_mails'

    def get_queryset(self):
        """
        Show all sent emails
        """
        return Message.objects.all()
            # .order_by('-time')


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Message
    login_url = '/users/login/'
    template_name = 'mail/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Message.objects.all()


class GroupMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='divers').exists()

class ComposeView(LoginRequiredMixin, GroupMixin, generic.FormView):
    template_name = 'mail/compose.html'
    login_url = '/users/login/'
    form_class = ComposeForm
    success_url = '/mail'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.sender = self.request.user
        model_instance = form.save(commit=True)
        model_instance.send()
        return super().form_valid(form)
