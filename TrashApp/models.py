from django.db import models
from restaurant.models import *
from SAAS.models import *
from PIL import Image

# importing datetime
from datetime import datetime, date



# Trash For Roles Model

class RolesTrashModel(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
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
        ordering = ["id"]
    
    def __str__(self):
        return str(self.id)


# Employee Trash Model

class EmployeeTrashModel(models.Model):
    STATUS_CHOICE = (
        ("ACTIVE", "ACTIVE"),
        ("BANN", "BANN")
    )
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=255)
    emp_username = models.CharField(max_length=255)
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


# Trash For selling session

class SellingSessionTrashModel(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    selling_session = models.ForeignKey(SellingSession, on_delete=models.SET_NULL, null=True)
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


# Trash For Customer Model
class CustomerTrashModel(models.Model):
    shop = models.ForeignKey(Shop, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    added_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    customer_contact = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_add = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.customer_email

# Trash for vendor

class VendorTrashModel(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
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
        return self.vendor_name


# trash models for brand

class BrandTrashModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    brand_name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # brand_img = models.ImageField(upload_to="images/")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.brand_name

# Category trash model

class CategoryTrashModel(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.category_name


# Item Trash model

class ItemTrashModel(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
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
        super(ItemTrashModel, self).save(*args, **kwargs)

        if not self.item_img:
            return

        imag = Image.open(self.item_img.path)
        if imag.width > 400 or imag.height > 400:
            output_size = (400, 400)
            imag.thumbnail(output_size)
            imag.save(self.item_img.path)


# Table trash model

class TableTrashModel(models.Model):
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, related_name="trashTable")
    table_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    waiter = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.table_name

# Restaurant main checkout or order trash model

class RestCheckoutTrashModel(models.Model):
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

    rest_checkout = models.ForeignKey(RestCheckout, on_delete=models.SET_NULL, null=True)
    sold_by = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(CartItems)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    grand_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    amount_received = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    change = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    status = models.CharField(max_length=255, null=True, choices=STATUS_CHOICE)
    payment_method = models.CharField(max_length=120, null=True, choices=PAYMENT_CHOICE, default="CASH")
    payment_number = models.CharField(max_length=120, null=True, blank=True)
    

    class Meta:
        ordering = ["-id"]
    

    def __str__(self):
        return str(self.id)
    
    def get_grand_total(self):
        return self.quantity * self.grand_total
    
    def save(self, *args, **kwargs):
        # self.change = self.amount_received - 
        if float(self.grand_total) > float(self.amount_received):
            self.change = decimal.Decimal(self.grand_total) - decimal.Decimal(self.amount_received)
        else:
            self.change = decimal.Decimal(self.amount_received) - decimal.Decimal(self.grand_total)
        if self.discount:
            discount = float(self.grand_total) * float(self.discount) / 100
            self.grand_total = float(self.grand_total) - discount
        super(RestCheckoutTrashModel, self).save(*args, **kwargs)


# due trash model

class DueTrashModel(models.Model):
    dueObj = models.ForeignKey(DueModel, on_delete=models.SET_NULL, null=True)
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

# refund trash model

class RefundTrashModel(models.Model):
    refundObj = models.ForeignKey(RefundModel, on_delete=models.SET_NULL, null=True)
    refund_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(RestCheckout, on_delete=models.SET_NULL, null=True)
    refund_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return str(self.id)


# advacne booking trash model

class AdvanceBookingTrashModel(models.Model):
    PAYMENT_METHOD = (
        ("CASH", "CASH"),
        ("CREDIT CARD", "CREDIT CARD"),
        ("PAYPAL", "PAYPAL"),
        ("BKASH", "BKASH"),
        ("NAGAD", "NAGAD"),
    )
    advanceBooking = models.ForeignKey(AdvanceBookingModel, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(default=datetime.now, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    customer_email = models.EmailField()
    notes = models.TextField(null=True, blank=True)
    number_of_people = models.PositiveIntegerField(default=1, null=True)
    advance_amount = models.IntegerField()
    method = models.CharField(max_length=255, null=True, default="CASH")
    account_number = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)
