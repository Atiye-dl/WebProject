# Generated by Django 5.0.6 on 2024-07-04 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Category',
            new_name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_available',
        ),
    ]
