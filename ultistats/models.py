from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def get_default(mod, default):
    """ get a default value for a model with unique field "name" """
    return mod.objects.get_or_create(name=default)[0]

class GameMode(models.Model):
    name = models.CharField(max_length=20)

class Pitch(models.Model):
    name = models.CharField(max_length=20)

class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    players = models.ManyToManyField(User)

class Score(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="score_team")
    hockey = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="score_hockey")
    assist = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="score_assist")
    score = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="score_score")

    # def limit_pub_date_choices(teaminstance):
    #     return {'user__in': teaminstance.players}

class Game(models.Model):
    date = models.DateField()
    mode = models.ForeignKey(GameMode, on_delete=models.CASCADE)
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    team_a = models.OneToOneField(Team, on_delete=models.CASCADE, related_name="game_team_a")
    team_b = models.OneToOneField(Team, on_delete=models.CASCADE, related_name="game_team_b")
