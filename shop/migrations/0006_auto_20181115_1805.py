# Generated by Django 2.1.3 on 2018-11-15 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20181115_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, to='shop.CartItem'),
        ),
    ]
