# Generated by Django 5.1.1 on 2024-09-23 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0029_trainerachievement"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainer",
            name="salary",
            field=models.IntegerField(default=0),
        ),
    ]
