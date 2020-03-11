from django.db import models
from django.conf import settings


# Create your models here.


class Profile(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.PROTECT)
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    gender = models.CharField(choices=(("d","divers"),
                                       ("f","female"),
                                       ("m","male")), max_length= 10)
    trikotnummer = models.CharField(max_length=3, null=True)
    email = models.EmailField()
    street = models.CharField(max_length=50, null=True)
    place = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=50, null=True)
