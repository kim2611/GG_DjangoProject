# Generated by Django 4.2.4 on 2023-08-16 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("k_sellboard", "0001_initial"),
        ("n_order", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="k_sellboard.product",
                verbose_name="상품",
            ),
        ),
    ]
