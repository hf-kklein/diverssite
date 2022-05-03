# Generated by Django 3.0.7 on 2020-11-04 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0010_auto_20200806_2359"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="location",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="events.Location"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="place",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="location",
            name="street",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
