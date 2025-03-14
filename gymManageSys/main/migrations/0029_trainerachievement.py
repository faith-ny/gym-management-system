# Generated by Django 5.1.1 on 2024-09-23 03:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0028_alter_banners_options_alter_notifuserstatus_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrainerAchievement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("detail", models.TextField()),
                ("img", models.ImageField(upload_to="trainers_achievements/")),
                (
                    "trainer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.trainer"
                    ),
                ),
            ],
        ),
    ]
