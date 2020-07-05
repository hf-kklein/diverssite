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

class ComposeForm(forms.Form):
    sender = forms.CharField()
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass