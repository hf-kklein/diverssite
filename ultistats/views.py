from django.shortcuts import render
from django.views import View
from .models import Game
from .forms import GameForm
from django.contrib.auth.models import User

class StatsFormView(View):
    def get(self, request):
        form = GameForm()
        players = User.objects.filter(is_active=True)

        context = {
            "form": form,
            "players": players.values_list("first_name", "last_name")
        }

        return render(request, "ultistats/index.html", context=context)