# Generated by Django 2.1.8 on 2020-06-28 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_report_input_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='input_lat',
            field=models.DecimalField(decimal_places=15, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='input_lon',
            field=models.DecimalField(decimal_places=15, max_digits=19, null=True),
        ),
    ]
