# Generated by Django 4.2.2 on 2023-08-04 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0018_alter_transactions_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_configs',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='app_configs',
            name='updated_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='scripts',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='scripts',
            name='updated_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='squredofftransactions',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='squredofftransactions',
            name='updated_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='token_log',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
