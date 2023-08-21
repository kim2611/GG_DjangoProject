# Generated by Django 4.2.4 on 2023-08-20 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("bcuser", "0002_bcuser_nickname"),
        ("o_mypage", "0004_alter_mypage_mypage_writer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mypage",
            name="mypage_writer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="bcuser.bcuser",
                verbose_name="작성자",
            ),
        ),
    ]