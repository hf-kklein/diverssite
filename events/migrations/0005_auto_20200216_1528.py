# Generated by Django 3.0.3 on 2020-02-16 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_auto_20200216_0111"),
    ]

    operations = [
        migrations.AlterField(
            model_name="participation",
            name="part",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="party", to="events.PartChoice"
            ),
        ),
    ]
