# Generated by Django 4.2.2 on 2023-08-04 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0017_alter_transactions_bidprice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]
