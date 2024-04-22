# Generated by Django 4.1.7 on 2023-06-29 17:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_alter_mtcpclient_date_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mtcpclient',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 29, 19, 53, 43, 210821)),
        ),
        migrations.AlterField(
            model_name='registers',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 29, 19, 53, 43, 211842)),
        ),
        migrations.AlterField(
            model_name='var',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 6, 29, 19, 53, 43, 209820)),
        ),
        migrations.AlterModelTable(
            name='value',
            table='value',
        ),
    ]
