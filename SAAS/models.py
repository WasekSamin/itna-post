from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from PIL import Image


class Currency(models.Model):
    currency_icon = models.CharField(max_length=10, null=True, unique=True)

    def __str__(self):
        return self.currency_icon

class Shop(models.Model):
    created_at = models.DateField(default=date.today)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255, unique=True)
    shop_address1 = models.TextField(null=True, blank=True)
    shop_address2 = models.TextField(null=True, blank=True)
    shop_contact = models.CharField(max_length=255, null=True)
    shop_bin_no = models.CharField(max_length=255, null=True, blank=True)
    shop_vat = models.CharField(max_length=255, null=True, blank=True)
    mushak_no = models.CharField(max_length=255, null=True, blank=True)
    shop_logo = models.ImageField(upload_to="images/", null=True)
    is_active = models.BooleanField(default=False, null=True)
    vat_amount = models.FloatField(null=True, default=0)
    show_mushak = models.BooleanField(default=False, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)


    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return self.shop_name
    
    @property
    def image_url(self):
        if self.shop_logo and hasattr(self.shop_logo, 'url'):
            return self.image.url

    def save(self, *args, **kwargs):
        super(Shop, self).save(*args, **kwargs)

        if not self.shop_logo:
            return

        imag = Image.open(self.shop_logo.path)
        if imag.width > 300 or imag.height> 300:
            output_size = (300, 300)
            imag.thumbnail(output_size)
            imag.save(self.shop_logo.path)




class Package(models.Model):
    package_name = models.CharField(max_length=255, unique=True)
    package_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration = models.PositiveIntegerField()
    package_description = models.TextField(null=True)

    def __str__(self):
        return self.package_name


class PackageCheckout(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    created_date = models.DateField(default=date.today)
    customer_obj = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=255)
    customer_phone_number = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, null=True, on_delete=models.SET_NULL)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bkash_number = models.CharField(max_length=16, null=True, blank=True)
    bkash_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    nagad_number = models.CharField(max_length=16, null=True, blank=True)
    nagad_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_expired = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return self.customer_name
    
