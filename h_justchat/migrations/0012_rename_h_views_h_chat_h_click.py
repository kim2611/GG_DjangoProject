# Generated by Django 4.2.4 on 2023-08-15 14:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("h_justchat", "0011_h_chat_h_views"),
    ]

    operations = [
        migrations.RenameField(
            model_name="h_chat",
            old_name="h_views",
            new_name="h_click",
        ),
    ]
