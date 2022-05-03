from django.contrib.auth.models import User
from django.forms import HiddenInput, ModelChoiceField, ModelForm, RadioSelect, formset_factory

from .models import PartChoice, Participation


class EventForm(ModelForm):
    part = ModelChoiceField(queryset=PartChoice.objects.all(), empty_label=None, required=False, widget=RadioSelect)

    class Meta:
        model = Participation
        fields = [
            "id",
            # "part",
            "event",
            "person",
        ]
        widgets = {
            "id": HiddenInput,
            # "part":RadioSelect,
            "event": HiddenInput,
            "person": HiddenInput,
        }
