# Generated by Django 3.2 on 2021-12-25 05:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('SAAS', '0001_initial'),
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=255)),
                ('tax_id', models.IntegerField(blank=True, null=True)),
                ('address', models.TextField(null=True)),
                ('zip_code', models.IntegerField(blank=True, null=True)),
                ('trade_license', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=255, null=True)),
                ('contact_name', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.citymodel')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.countrymodel')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.vendor')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TableTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trashTable', to='restaurant.table')),
                ('waiter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.employee')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SellingSessionTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening_date', models.DateField(default=datetime.date.today)),
                ('opening_text', models.CharField(blank=True, max_length=255, null=True)),
                ('closing_text', models.CharField(blank=True, max_length=255, null=True)),
                ('total_sold', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('closing_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('selling_session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.sellingsession')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RolesTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_title', models.CharField(max_length=255)),
                ('is_admin', models.BooleanField(default=False, null=True)),
                ('can_config_pos', models.BooleanField(default=False, null=True)),
                ('can_config_roles', models.BooleanField(default=False, null=True)),
                ('can_config_orders', models.BooleanField(default=False, null=True)),
                ('can_config_inventory', models.BooleanField(default=False, null=True)),
                ('can_config_customers', models.BooleanField(default=False, null=True)),
                ('can_config_vendors', models.BooleanField(default=False, null=True)),
                ('can_config_tables', models.BooleanField(default=False, null=True)),
                ('can_config_emps', models.BooleanField(default=False, null=True)),
                ('can_manage_settings', models.BooleanField(default=False, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.roles')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RestCheckoutTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('discount', models.IntegerField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('amount_received', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(choices=[('PAID', 'PAID'), ('UNPAID', 'UNPAID')], max_length=255, null=True)),
                ('payment_method', models.CharField(choices=[('CASH', 'CASH'), ('Credit Card', 'Credit Card'), ('bKash', 'bKash'), ('Nagad', 'Nagad')], default='CASH', max_length=120, null=True)),
                ('payment_number', models.CharField(blank=True, max_length=120, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.customer')),
                ('items', models.ManyToManyField(to='restaurant.CartItems')),
                ('rest_checkout', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.restcheckout')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
                ('sold_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.employee')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RefundTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refund_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.restcheckout')),
                ('refundObj', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.refundmodel')),
                ('refund_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.employee')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ItemTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('item_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('buying_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('stock_amount', models.PositiveIntegerField(default=0)),
                ('out_of_stock', models.BooleanField(blank=True, default=False, null=True)),
                ('item_img', models.ImageField(null=True, upload_to='images/')),
                ('product_descriptions', models.TextField(null=True)),
                ('upc', models.IntegerField(blank=True, null=True)),
                ('sku', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.brand')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.category')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.item')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.vendor')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('emp_username', models.CharField(max_length=255)),
                ('emp_pin', models.CharField(max_length=255)),
                ('confirm_pin', models.CharField(max_length=255, null=True)),
                ('emp_profile_pic', models.ImageField(upload_to='images/')),
                ('is_active', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('BANN', 'BANN')], max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.employee')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.roles')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DueTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('order_note', models.TextField()),
                ('submission_date', models.DateField()),
                ('due_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('due_grand_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('due_clear', models.BooleanField(default=False, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.customer')),
                ('dueObj', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.duemodel')),
                ('items', models.ManyToManyField(to='restaurant.CartItems')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
                ('sold_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.employee')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CustomerTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_contact', models.CharField(max_length=255)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_add', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.employee')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.customer')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CategoryTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.category')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='BrandTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.brand')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='AdvanceBookingTrashModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(default=datetime.datetime.now, null=True)),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_phone', models.CharField(max_length=255)),
                ('customer_email', models.EmailField(max_length=254)),
                ('notes', models.TextField(blank=True, null=True)),
                ('number_of_people', models.PositiveIntegerField(default=1, null=True)),
                ('advance_amount', models.IntegerField()),
                ('method', models.CharField(default='CASH', max_length=255, null=True)),
                ('account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('advanceBooking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.advancebookingmodel')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SAAS.shop')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
