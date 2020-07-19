from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
def user_profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile/user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional information not contained in base user
    gender = models.CharField(choices=(("d", "divers"),
                                       ("f", "female"),
                                       ("m", "male")), max_length=10, null=True,
                              blank=True)
    trikotnummer = models.CharField(max_length=3, null=True, unique=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    place = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to=user_profile_directory_path, null=True, blank=True)
