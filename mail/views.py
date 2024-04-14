from email.utils import parseaddr
from json import dumps
from urllib import request

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View, generic

from .forms import ComposeForm
from .models import Message


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = "/users/login/"
    template_name = "mail/index.html"
    context_object_name = "sent_mails"

    def get_queryset(self):
        """
        Show all sent emails
        """
        return Message.objects.all()
        # .order_by('-time')


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Message
    login_url = "/users/login/"
    template_name = "mail/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Message.objects.all()


class GroupMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="divers").exists()


class ComposeView(LoginRequiredMixin, GroupMixin, generic.FormView):
    template_name = "mail/compose.html"
    login_url = "/users/login/"
    form_class = ComposeForm
    success_url = "/mail"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        qd = self.request.POST  # obtain the querydict of the POST request
        form.instance.sender = self.request.user

        model_instance = form.save(commit=True)
        recip_input = qd.getlist("recipients")
        recip_email = [parseaddr(r)[1] for r in recip_input]
        recipients = User.objects.filter(email__in=recip_email)

        if qd.get("send_to_active", default="off") == "on":
            newrecip = User.objects.filter(is_active=True)
            recipients = recipients.union(newrecip)

        if qd.get("send_to_all", default="off") == "on":
            newrecip = User.objects.all()
            recipients = recipients.union(newrecip)

        form.instance.recipients.set(recipients)
        model_instance = form.save(commit=True)
        print("so far all went well")
        model_instance.send()
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # print(form)
        return response

    def get(self, request):
        form = ComposeForm()
        recipients = User.objects.exclude(username="admin").values_list("first_name", "last_name", "email")
        recipients = ["{} {} <{}>".format(r[0], r[1], r[2]) for r in recipients]
        print(recipients)
        context = {"form": form, "search_data": dumps(list(recipients))}
        return render(request, self.template_name, context)
