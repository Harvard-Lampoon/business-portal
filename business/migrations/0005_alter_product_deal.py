# Generated by Django 4.0 on 2021-12-25 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_rename_contract_product_deal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='deal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deals', to='business.deal'),
        ),
    ]
