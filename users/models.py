from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional information not contained in base user
    gender = models.CharField(choices=(("d","divers"),
                                       ("f","female"),
                                       ("m","male")), max_length= 10, null = True)
    trikotnummer = models.CharField(max_length=3, null=True, unique = True)
    street = models.CharField(max_length=50, null=True)
    place = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=50, null=True)
