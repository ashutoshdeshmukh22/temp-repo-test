# Generated by Django 4.2.1 on 2023-06-21 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0003_token_log_encrypted_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_configs',
            name='value',
            field=models.CharField(max_length=500),
        ),
    ]
