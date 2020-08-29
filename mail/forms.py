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
from .models import Message
from django.conf import settings


class ComposeForm(forms.ModelForm):
    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

    class Meta:
        model = Message
        fields = ['recipients', 'subject', 'body']
        widgets = {
            'recipients': forms.CheckboxSelectMultiple()
        }

