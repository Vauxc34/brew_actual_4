# Generated by Django 5.0.6 on 2024-08-09 11:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0020_alter_mtcpclient_date_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mtcpclient',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 8, 9, 11, 5, 5, 104274)),
        ),
        migrations.AlterField(
            model_name='registers',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 8, 9, 11, 5, 5, 104765)),
        ),
        migrations.AlterField(
            model_name='var',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 8, 9, 11, 5, 5, 103201)),
        ),
    ]
