# Generated by Django 4.0 on 2021-12-26 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_other'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
    ]
