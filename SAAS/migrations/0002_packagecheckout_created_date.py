# Generated by Django 3.2 on 2022-01-07 15:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAAS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagecheckout',
            name='created_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
