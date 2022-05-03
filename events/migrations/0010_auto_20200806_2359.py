# Generated by Django 3.0.7 on 2020-08-06 21:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0009_remove_event_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="author",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="slug",
            field=models.SlugField(editable=False, null=True),
        ),
    ]
