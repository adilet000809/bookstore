# Generated by Django 2.1.3 on 2018-12-04 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20181129_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Cart'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Waiting for the recipient', 'Waiting for the recipient'), ('Handed over', 'Handed over')], default='Accepted', max_length=100),
        ),
    ]
