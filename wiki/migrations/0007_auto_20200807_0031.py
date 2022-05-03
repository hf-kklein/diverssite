# Generated by Django 3.0.7 on 2020-08-06 22:31

from django.db import migrations, models
import wiki.models


class Migration(migrations.Migration):

    dependencies = [
        ("wiki", "0006_auto_20200303_2118"),
    ]

    operations = [
        migrations.AddField(
            model_name="articles",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to=wiki.models.file_directory_path),
        ),
        migrations.AddField(
            model_name="articles",
            name="picture",
            field=models.ImageField(blank=True, null=True, upload_to=wiki.models.file_directory_path),
        ),
    ]
