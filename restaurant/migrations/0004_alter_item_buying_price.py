# Generated by Django 3.2 on 2022-01-04 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20220104_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='buying_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
