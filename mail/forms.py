# created by Florian Schunck on 05.07.2020
# Project: diverssite
# Short description of the feature:
#
#
# ------------------------------------------------------------------------------
# Open tasks:
# TODO:
#
# ------------------------------------------------------------------------------
from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from .models import Message


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, user):
        if user.first_name == "" and user.last_name == "":
            return user.email
        return " ".join([user.first_name, user.last_name])


class ComposeForm(forms.ModelForm):
    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

    class Meta:
        model = Message
        fields = ["subject", "body"]
        # widgets = {
        #     'recipients': forms.CheckboxSelectMultiple()
        # }

    # recipients = CustomMMCF(
    #     queryset=User.objects.exclude(username='admin'),
    #     widget=forms.CheckboxSelectMultiple
    # )
