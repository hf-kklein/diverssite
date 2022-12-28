# script to save model instances. THis is done to invoke save() method of models
# to update older entries in databases

from wiki.models import Image
from users.models import Profile


def run():
    images = Image.objects.all()
    for img in images:
        img.save()

    profiles = Profile.objects.all()
    for pro in profiles:
        pro.save()
