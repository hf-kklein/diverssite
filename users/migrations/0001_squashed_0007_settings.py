# Generated by Django 3.0.7 on 2021-02-14 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    replaces = [
        ("users", "0001_initial"),
        ("users", "0002_auto_20200322_1927"),
        ("users", "0003_profile_picture"),
        ("users", "0004_auto_20200719_1603"),
        ("users", "0005_auto_20200722_1800"),
        ("users", "0006_auto_20200722_1910"),
        ("users", "0007_settings"),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "gender",
                    models.CharField(
                        blank=True, choices=[("d", "divers"), ("f", "female"), ("m", "male")], max_length=10, null=True
                    ),
                ),
                ("trikotnummer", models.CharField(blank=True, max_length=3, null=True, unique=True)),
                ("street", models.CharField(blank=True, max_length=50, null=True)),
                ("place", models.CharField(blank=True, max_length=50, null=True)),
                ("zip", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
                (
                    "picture",
                    models.ImageField(blank=True, null=True, upload_to=users.models.user_profile_directory_path),
                ),
                ("mobile", models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Settings",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "registration_password",
                    models.CharField(help_text="Passwort wird bei der Registrierung abgefragt", max_length=20),
                ),
            ],
        ),
    ]
