# Generated by Django 4.2.7 on 2023-11-25 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_alter_cart_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='is_purchased',
            new_name='is_ordered',
        ),
    ]
