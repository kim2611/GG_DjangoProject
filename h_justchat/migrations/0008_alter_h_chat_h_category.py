# Generated by Django 4.2.4 on 2023-08-14 10:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("h_justchat", "0007_alter_h_chat_h_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="h_chat",
            name="h_category",
            field=models.CharField(
                choices=[("소식", "소식"), ("친목", "친목"), ("기타", "기타")],
                default="news",
                max_length=64,
                verbose_name="카테고리",
            ),
        ),
    ]