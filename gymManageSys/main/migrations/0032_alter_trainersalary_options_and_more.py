# Generated by Django 5.1.1 on 2024-09-23 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0031_trainersalary"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="trainersalary",
            options={"verbose_name_plural": "Trainer Salary"},
        ),
        migrations.AlterField(
            model_name="trainersalary",
            name="remarks",
            field=models.TextField(blank=True),
        ),
    ]
