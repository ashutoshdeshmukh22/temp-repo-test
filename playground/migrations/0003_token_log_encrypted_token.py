# Generated by Django 4.2.1 on 2023-06-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0002_token_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='token_log',
            name='encrypted_token',
            field=models.CharField(default='ok', max_length=300),
            preserve_default=False,
        ),
    ]
