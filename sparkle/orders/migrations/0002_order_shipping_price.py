# Generated by Django 5.0.6 on 2024-07-06 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
