from django.contrib.auth.models import User
from django.forms import ModelForm, ModelMultipleChoiceField, DateInput, TextInput
from .models import Game, Score, Team



class GameForm(ModelForm):
    team_a = ModelMultipleChoiceField(
        User.objects.filter(is_active=True),
        widget=TextInput
        )
    class Meta:
        model = Game
        fields = [
            "date",
            "mode",
            "pitch",
        ]
        widgets = {
            "date": DateInput
            }