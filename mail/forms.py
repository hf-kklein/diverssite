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
from django.contrib.auth.models import User

class CustomMMCF(forms.ModelMultipleChoiceField):    
    def label_from_instance(self, user):
        print(user.first_name == "" and user.last_name == "")
        if user.first_name == "" and user.last_name == "":
            print("test")
            return user.email
        return " ".join([user.first_name, user.last_name])

class ComposeForm(forms.ModelForm):
    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

    class Meta:
        model = Message
        fields = ['recipients', 'subject', 'body']
        # widgets = {
        #     'recipients': forms.CheckboxSelectMultiple()
        # }

    recipients = CustomMMCF(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
