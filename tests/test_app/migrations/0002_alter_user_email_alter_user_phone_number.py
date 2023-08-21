# Generated by Django 4.1.6 on 2023-02-09 06:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("test_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(max_length=32, null=True),
        ),
    ]
