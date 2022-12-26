from django import forms
from django.forms.widgets import CheckboxSelectMultiple


class ArticleAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            "category": CheckboxSelectMultiple,
            "show_on_pages": CheckboxSelectMultiple,
        }
