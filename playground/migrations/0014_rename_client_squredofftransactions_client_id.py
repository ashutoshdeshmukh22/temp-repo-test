# Generated by Django 4.2.2 on 2023-07-09 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0013_alter_squredofftransactions_client'),
    ]

    operations = [
        migrations.RenameField(
            model_name='squredofftransactions',
            old_name='client',
            new_name='client_id',
        ),
    ]
