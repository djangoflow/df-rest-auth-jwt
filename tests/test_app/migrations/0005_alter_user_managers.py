# Generated by Django 4.1.6 on 2023-07-14 09:56

from django.db import migrations
import tests.test_app.models


class Migration(migrations.Migration):
    dependencies = [
        ("test_app", "0004_remove_user_username"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", tests.test_app.models.UserManager()),
            ],
        ),
    ]
