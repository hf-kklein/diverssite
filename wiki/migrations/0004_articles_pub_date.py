# Generated by Django 3.0.3 on 2020-02-29 00:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("wiki", "0003_articles_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="articles",
            name="pub_date",
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
