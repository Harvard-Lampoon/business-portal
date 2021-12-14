# Generated by Django 4.0 on 2021-12-14 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('release_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('cash', 'Cash'), ('trade', 'Trade')], max_length=50)),
                ('status', models.CharField(choices=[('created', 'Created'), ('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], max_length=50)),
                ('value', models.DecimalField(decimal_places=2, max_digits=50)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('signed_at', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.user')),
                ('issue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.issue')),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('quarter', 'Quarter Page'), ('half', 'Half Page'), ('full', 'Full Page'), ('two', 'Two Page Spread')], max_length=255)),
                ('placement', models.CharField(choices=[('inside_front', 'Inside Front Cover'), ('opposite_inside_front', 'Opposite Inside Front Cover'), ('inside_back', 'Inside Back Cover'), ('opposite_inside_back', 'Opposite Inside Back Cover'), ('back', 'Back Cover'), ('two_page_centerfold', 'Two Page Centerfold Spread')], max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='ads/')),
                ('is_color', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.deal')),
            ],
        ),
    ]
