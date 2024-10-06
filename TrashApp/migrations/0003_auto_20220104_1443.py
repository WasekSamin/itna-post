# Generated by Django 3.2 on 2022-01-04 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrashApp', '0002_alter_itemtrashmodel_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtrashmodel',
            name='buying_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='itemtrashmodel',
            name='item_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='itemtrashmodel',
            name='product_descriptions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='itemtrashmodel',
            name='sku',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
