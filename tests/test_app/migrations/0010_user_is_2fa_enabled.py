# Generated by Django 4.2.4 on 2023-09-05 05:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("test_app", "0009_rename_created_by_user_invited_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_2fa_enabled",
            field=models.BooleanField(default=False),
        ),
    ]
