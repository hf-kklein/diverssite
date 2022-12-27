import io
import os
import PIL
from PIL import ImageOps
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File


# Create your models here.
def user_profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print(filename)
    return "profile/user_{0}/{1}".format(instance.user.id, filename)


def file_directory_path_tumbnail(instance, filename):
    path = user_profile_directory_path(instance, filename)
    head, ext = os.path.splitext(path)
    return f"{head}-thumb{ext}"


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
    thumbnail = models.ImageField(
        upload_to=file_directory_path_tumbnail,
        default="/static/images/default_profile_thumbnail.png",  #
        editable=False,
    )

    def image_url(self):
        """
        Returns the URL of the image associated with this Object.
        If an image hasn't been uploaded yet, it returns a stock image

        :returns: str -- the image url

        """
        default = "/static/images/default_profile.png"
        if self.picture and hasattr(self.picture, "url"):
            if default in self.picture.url:
                return default
            return self.picture.url
        else:
            return default

    def thumb_url(self):
        """
        Returns the URL of the image associated with this Object.
        If an image hasn't been uploaded yet, it returns a stock image

        :returns: str -- the image url

        """
        default = "/static/images/default_profile_thumbnail.png"

        if self.thumbnail and hasattr(self.thumbnail, "url"):
            if default in self.thumbnail.url:
                return default
            return self.thumbnail.url
        else:
            return default

    def save(self, *args, **kwargs):
        if not self.picture:
            self.thumbnail = None
        else:
            # extract path from old file and append thumbnail
            thumb_path = file_directory_path_tumbnail(self, os.path.basename(self.picture.path))

            # create byte buffer
            buf = io.BytesIO()

            # open original image, transpose to address exif tags,
            # resize and save to buffer
            thumbnail_size = 100, 100
            tiny_img = PIL.Image.open(self.picture)
            tiny_img = ImageOps.exif_transpose(tiny_img)
            tiny_img.thumbnail(thumbnail_size)
            tiny_img.save(buf, format="JPEG")

            # save new objects to thumbnail field
            self.thumbnail.file = File(buf)
            self.thumbnail.name = thumb_path

            # save image to media with thumbnail path property
            tiny_img.save(self.thumbnail.path, format="JPEG")

        super(Profile, self).save(*args, **kwargs)

    # def __str__(self):
    #     return self.user.name
