# Generated by Django 4.0 on 2021-12-30 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docusign', '0002_apiclient_refresh_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiclient',
            name='access_token',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]