# Generated by Django 5.0.6 on 2024-07-27 12:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_alter_mtcpclient_date_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mtcpclient',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 27, 12, 56, 28, 730659)),
        ),
        migrations.AlterField(
            model_name='registers',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 27, 12, 56, 28, 731125)),
        ),
        migrations.AlterField(
            model_name='var',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 27, 12, 56, 28, 729617)),
        ),
    ]
