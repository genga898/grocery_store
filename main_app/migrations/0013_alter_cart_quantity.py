# Generated by Django 4.2.7 on 2023-11-23 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_product_shipping_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]