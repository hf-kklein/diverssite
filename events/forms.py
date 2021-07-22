from .models import Participation, PartChoice
from django.contrib.auth.models import User
from django.forms import ModelForm, formset_factory, RadioSelect, HiddenInput, ModelChoiceField

class EventForm(ModelForm):
    part = ModelChoiceField(
        queryset=PartChoice.objects.all(),
        empty_label=None, required=False,
        widget=RadioSelect)

    class Meta:
        model = Participation
        fields = [
            "id",
            # "part",
            "event",
            "person"
        ]
        widgets = {
            "id": HiddenInput,
            # "part":RadioSelect,
            "event": HiddenInput,
            "person": HiddenInput
        }

