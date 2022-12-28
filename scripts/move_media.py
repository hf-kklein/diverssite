# moves media files which were placed before update of naming function
import glob
import shutil
from wiki.models import Image, File, file_directory_path, file_directory_path_tumbnail
from django.conf import settings


def trim_leading_slash(url):
    if url[0] == "/":
        return url[1:]
    return url


def run():
    media = trim_leading_slash(settings.MEDIA_URL)
    
    # move images
    images = Image.objects.all()

    mediafiles = glob.glob("media/wiki/image*")
    for img in images:
        old_path = trim_leading_slash(img.file.url)
        if old_path in mediafiles:
            new_path = file_directory_path(img, img.file.name)
            img.file.name = new_path
            _ = shutil.move(old_path, trim_leading_slash(img.file.url))
            img.save()

    # move files
    files = File.objects.all()

    mediafiles = glob.glob("media/wiki/file*")
    for f in files:
        old_path = trim_leading_slash(f.file.url)
        if old_path in mediafiles:
            new_path = file_directory_path(f, f.file.name)
            f.file.name = new_path
            _ = shutil.move(old_path, trim_leading_slash(f.file.url))
            img.save()