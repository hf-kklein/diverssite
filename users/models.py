from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Create your models here.
def user_profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print(filename)
    return "profile/user_{0}/{1}".format(instance.user.id, filename)


class Settings(models.Model):
    registration_password = models.CharField(max_length=20, help_text="Passwort wird bei der Registrierung abgefragt")

    def __str__(self):
        return "User Settings"

    def save(self, *args, **kwargs):
        if not self.pk and Settings.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError("Nur bestehender Eintrag kann geändert werden")
        return super(Settings, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional information not contained in base user
    gender = models.CharField(
        choices=(("d", "divers"), ("f", "female"), ("m", "male")), max_length=10, null=True, blank=True
    )
    trikotnummer = models.CharField(max_length=3, null=True, unique=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    place = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to=user_profile_directory_path, null=True, blank=True)

    def image_url(self):
        """
        Returns the URL of the image associated with this Object.
        If an image hasn't been uploaded yet, it returns a stock image

        :returns: str -- the image url

        """
        if self.picture and hasattr(self.picture, "url"):
            return self.picture.url
        else:
            return "/static/images/default_profile.png"

    #
    # def __str__(self):
    #     return self.user.name
