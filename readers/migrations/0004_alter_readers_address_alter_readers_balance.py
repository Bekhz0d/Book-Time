# Generated by Django 5.0 on 2023-12-31 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readers', '0003_readers_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readers',
            name='address',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='readers',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8),
        ),
    ]