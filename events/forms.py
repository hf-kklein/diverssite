from .models import Participation
from django.contrib.auth.models import User
from django.forms import ModelForm, formset_factory, RadioSelect, HiddenInput

class EventForm(ModelForm):
    class Meta:
        model = Participation
        fields = [
            "id",
            "event",
            "part",
            "person"
        ]
        widgets = {
            "id": HiddenInput,
            "part": RadioSelect,
            "event": HiddenInput,
            "person": HiddenInput
        }

