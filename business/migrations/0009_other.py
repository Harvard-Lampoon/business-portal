# Generated by Django 4.0 on 2021-12-26 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0008_alter_product_deal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Other',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='business.product')),
            ],
            bases=('business.product',),
        ),
    ]
