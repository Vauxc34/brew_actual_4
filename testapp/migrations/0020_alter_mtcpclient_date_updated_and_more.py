# Generated by Django 5.0.6 on 2024-08-09 10:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0019_remove_var_action_remove_var_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mtcpclient',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 8, 9, 10, 49, 31, 238143)),
        ),
        migrations.AlterField(
            model_name='registers',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 8, 9, 10, 49, 31, 238610)),
        ),
        migrations.AlterField(
            model_name='var',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 8, 9, 10, 49, 31, 237044)),
        ),
    ]
