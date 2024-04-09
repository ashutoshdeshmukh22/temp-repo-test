# Generated by Django 4.2.2 on 2023-06-29 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0005_alter_app_configs_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scripts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('script_code', models.PositiveIntegerField(default=0)),
                ('tradingSymbol', models.CharField(default='', max_length=100)),
                ('lotSize', models.PositiveIntegerField(default=1)),
                ('multiplier', models.PositiveIntegerField()),
                ('status', models.BooleanField(default=False)),
                ('optionType', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
