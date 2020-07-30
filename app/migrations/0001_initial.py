# Generated by Django 2.1.8 on 2020-07-30 22:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_report', models.CharField(default='비어있음', max_length=200, null=True)),
                ('input_date', models.CharField(blank=True, default=0, max_length=20, null=True)),
                ('input_time', models.CharField(blank=True, default=0, max_length=20, null=True)),
                ('input_lat', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('input_lon', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('input_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
