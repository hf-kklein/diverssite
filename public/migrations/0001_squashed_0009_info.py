# Generated by Django 3.0.7 on 2021-02-14 13:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('public', '0001_initial'), ('public', '0002_auto_20200207_0917'), ('public', '0003_post_visibility'), ('public', '0004_auto_20200208_0829'), ('public', '0005_auto_20200209_0107'), ('public', '0006_auto_20200209_0145'), ('public', '0007_auto_20200209_0202'), ('public', '0008_delete_post'), ('public', '0009_info')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('welcome_title', models.TextField(blank=True, null=True)),
                ('welcome_text', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
