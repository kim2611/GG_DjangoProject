# Generated by Django 4.2.4 on 2023-08-09 05:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("h_justchat", "0003_alter_h_chat_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="h_chat",
            name="h_register_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="등록날짜"
            ),
        ),
    ]
