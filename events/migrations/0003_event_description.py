# Generated by Django 3.0.2 on 2020-02-11 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20200208_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
