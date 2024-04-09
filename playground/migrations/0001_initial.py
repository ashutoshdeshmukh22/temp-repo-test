# Generated by Django 4.2.1 on 2023-06-11 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='app_configs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('client_id', models.CharField(default='', max_length=100, primary_key=True, serialize=False)),
                ('limit', models.IntegerField(default=30000)),
                ('phone', models.CharField(max_length=12, null=True)),
                ('note', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('transaction_id', models.CharField(default='', editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('script_code', models.CharField(default='', max_length=100)),
                ('name', models.CharField(default='', max_length=100)),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('action', models.CharField(choices=[('Buy', 'Buy'), ('Sell', 'Sell')], default='Buy', max_length=5)),
                ('created_by', models.CharField(default='', max_length=50)),
                ('updated_by', models.CharField(default='', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playground.clientprofile')),
            ],
        ),
    ]