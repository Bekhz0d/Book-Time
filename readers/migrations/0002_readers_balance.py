# Generated by Django 5.0 on 2023-12-31 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='readers',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]