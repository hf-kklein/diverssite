# Generated by Django 3.1.12 on 2022-12-26 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_squashed_0012_auto_20201105_1738"),
        ("wiki", "0006_auto_20221226_1758"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="event",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="events.event"
            ),
        ),
    ]
