# Generated by Django 2.1.8 on 2020-06-27 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='input_report',
            field=models.CharField(default='비어있음', max_length=200, null=True),
        ),
    ]
