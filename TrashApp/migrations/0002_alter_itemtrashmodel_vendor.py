# Generated by Django 3.2 on 2021-12-26 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_alter_item_vendor'),
        ('TrashApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtrashmodel',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.vendor'),
        ),
    ]