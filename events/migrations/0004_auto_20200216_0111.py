# Generated by Django 3.0.3 on 2020-02-16 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20200216_0102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participation',
            old_name='participation',
            new_name='part',
        ),
    ]
