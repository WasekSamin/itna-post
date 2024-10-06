from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from PIL import Image
import decimal
from SAAS.models import Shop
from datetime import datetime


# Create your models here.
class Roles(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, null=True)
    role_title = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False, null=True)
    can_config_pos = models.BooleanField(default=False, null=True)
    can_config_roles = models.BooleanField(default=False, null=True)
    can_config_orders = models.BooleanField(default=False, null=True)
    can_config_inventory = models.BooleanField(default=False, null=True)
    can_config_customers = models.BooleanField(default=False, null=True)
    can_config_vendors = models.BooleanField(default=False, null=True)
    can_config_tables = models.BooleanField(default=False, null=True)
    can_config_emps = models.BooleanField(default=False, null=True)
    can_manage_settings = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)
    updated_at = models.DateTimeField(default=datetime.now, null=True)

    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return str(self.id)



class Employee(models.Model):
    STATUS_CHOICE = (
        ("ACTIVE", "ACTIVE"),
        ("BANN", "BANN")
    )
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=255)
    emp_username = models.CharField(max_length=255, unique=True)
    emp_pin = models.CharField(max_length=255)
    confirm_pin = models.CharField(max_length=255, null=True)
    emp_profile_pic = models.ImageField(upload_to="images/")
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    is_active = models.CharField(max_length=255, null=True, choices=STATUS_CHOICE)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return self.emp_username


class SellingSession(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    opening_date = models.DateField(default=date.today)
    opening_text = models.CharField(max_length=255, null=True, blank=True)
    closing_text = models.CharField(max_length=255, null=True, blank=True)
    total_sold = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    closing_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.opening_date)


class Customer(models.Model):
    shop = models.ForeignKey(Shop, null=True, on_delete=models.SET_NULL)
    added_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    customer_contact = models.CharField(max_length=255)
    customer_email = models.EmailField(unique=True)
    customer_add = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.customer_email


class CountryModel(models.Model):
    country_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return self.country_name


class CityModel(models.Model):
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return self.city_name


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255)
    tax_id = models.IntegerField(null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    address = models.TextField(null=True)
    country = models.ForeignKey(CountryModel, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(CityModel, on_delete=models.SET_NULL, null=True)
    zip_code = models.IntegerField(null=True, blank=True)
    trade_license = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True)
    contact_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)


class Brand(models.Model):
    brand_name = models.CharField(max_length=255, unique=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # brand_img = models.ImageField(upload_to="images/")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.category_name


class SellingType(models.Model):
    type_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.type_name


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    buying_price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    stock_amount = models.PositiveIntegerField(default=0)
    out_of_stock = models.BooleanField(default=False, null=True, blank=True)
    item_img = models.ImageField(upload_to="images/", null=True, blank=True)
    product_descriptions = models.TextField(null=True, blank=True)
    upc = models.IntegerField(null=True, blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

        if not self.item_img:
            return

        imag = Image.open(self.item_img.path)
        if imag.width > 400 or imag.height > 400:
            output_size = (400, 400)
            imag.thumbnail(output_size)
            imag.save(self.item_img.path)

    @property
    def get_items_by_category(self):
        return Item.objects.filter(category__item_name=self.title)

    @staticmethod
    def get_items(ids):
        return Item.objects.filter(id__in=ids)


class Table(models.Model):
    table_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    number_of_chairs = models.PositiveIntegerField(default=1, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    waiter = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.id)


class TableItems(models.Model):
    items = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)


class CartItems(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-id"]


class TableCheckout(models.Model):
    STATUS_CHOICES = (
        ("PAID", "PAID"),
        ("UNPAID", "UNPAID")
    )
    sold_by = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    created_at = models.DateField(default=date.today, null=True)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    item_item = models.ManyToManyField(TableItems)
    table_status = models.CharField(max_length=255, null=True, choices=STATUS_CHOICES)
    discount = models.FloatField(null=True)
    amount_received = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    change = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    grand_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     # self.change = self.amount_received - 
    #     if float(self.total) > float(self.amount_received):
    #             self.change = decimal.Decimal(self.total) - decimal.Decimal(self.amount_received)
    #     else:
    #         self.change = decimal.Decimal(self.amount_received) - decimal.Decimal(self.total)
    #     if self.discount:
    #             discount = float(self.total) * float(self.discount) / 100
    #             self.total = float(self.total) - discount
    #     super(TableCheckout, self).save(*args, **kwargs)

class RestCheckout(models.Model):
    STATUS_CHOICE = (
        ("PAID", "PAID"),
        ("UNPAID", "UNPAID")
    )
    PAYMENT_CHOICE = (
        ("CASH", "CASH"),
        ("Credit Card", "Credit Card"),
        ("bKash", "bKash"),
        ("Nagad", "Nagad")
    )

    sold_by = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=datetime.now)
    created_date = models.DateField(default=date.today)
    updated_at = models.DateTimeField(default=datetime.now)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(CartItems)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    grand_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    amount_received = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    change = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, null=True)
    status = models.CharField(max_length=255, null=True, choices=STATUS_CHOICE)
    payment_method = models.CharField(max_length=120, null=True, choices=PAYMENT_CHOICE, default="CASH")
    payment_number = models.CharField(max_length=120, null=True, blank=True)
    

    class Meta:
        ordering = ["-id"]
    

    def __str__(self):
        return str(self.id)
    
    def get_grand_total(self):
        return self.quantity * self.grand_total
    
    # def save(self, *args, **kwargs):
        # if float(self.grand_total) > float(self.amount_received):
        #     self.change = decimal.Decimal(self.grand_total) - decimal.Decimal(self.amount_received)
        # else:
        #     self.change = decimal.Decimal(self.amount_received) - decimal.Decimal(self.grand_total)
        # if self.discount:
        #     discount = float(self.grand_total) * float(self.discount) / 100
        #     self.grand_total = float(self.grand_total) - discount
        # super(RestCheckout, self).save(*args, **kwargs)


class DueModel(models.Model):
    sold_by = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order_note = models.TextField()
    submission_date = models.DateField()
    items = models.ManyToManyField(CartItems)
    due_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    due_grand_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    due_clear = models.BooleanField(default=False, null=True)
    

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)


class RefundModel(models.Model):
    refund_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(RestCheckout, on_delete=models.SET_NULL, null=True)
    refund_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return str(self.id)


class AdvanceBookingModel(models.Model):
    PAYMENT_METHOD = (
        ("CASH", "CASH"),
        ("CREDIT CARD", "CREDIT CARD"),
        ("PAYPAL", "PAYPAL"),
        ("BKASH", "BKASH"),
        ("NAGAD", "NAGAD"),
    )
    created_at = models.DateField(default=datetime.now, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    customer_email = models.EmailField()
    notes = models.TextField(null=True, blank=True)
    number_of_people = models.PositiveIntegerField(default=1, null=True)
    advance_amount = models.IntegerField()
    method = models.CharField(max_length=255, null=True, default="CASH", choices=PAYMENT_METHOD)
    account_number = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)


#if len(credit_card_number) > 0 or len(bkash_number) or len(nagad_number):
        #     if len(credit_card_number) > 0:
        #         payment_method = "Credit Card"
        #         payment_number = credit_card_number
        #     elif len(bkash_number) > 0:
        #         payment_method = "bKash"
        #         payment_number = bkash_number
        #     elif len(nagad_number) > 0:
        #         payment_method = "Nagad"
        #         payment_number = nagad_number
        # else:
        #     payment_method="CASH"