# Generated by Django 4.2.2 on 2023-06-30 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0007_scripts_expirydate'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='bidPrice',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='transactions',
            name='expirydate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='transactions',
            name='multiplier',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='transactions',
            name='offerPrice',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='transactions',
            name='status',
            field=models.BooleanField(choices=[(True, 'Active'), (False, 'Closed')], default=True, null=True),
        ),
        migrations.AlterField(
            model_name='scripts',
            name='expiryDate',
            field=models.DateField(),
        ),
    ]