from django.db import models
from SAAS.models import *
from restaurant.models import Vendor
# Create your models here.
class MedicineCategory(models.Model):
    med_cat_name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)


    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.med_cat_name


class MedicineBrand(models.Model):
    med_brand_name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    med_brand_logo = models.ImageField(upload_to="images/")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.med_brand_name

    @property
    def imageURL(self):
        try:
            url = self.med_brand_logo.url
        except:
            url = ""
        return url


class MedicinePower(models.Model):
    power_amount = models.CharField(max_length=255)

    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return self.power_amount


class Medicine(models.Model):
    med_name = models.CharField(max_length=255)
    med_image = models.ImageField(upload_to="images/")
    med_category = models.ForeignKey(MedicineCategory, on_delete=models.SET_NULL, null=True)
    med_brand = models.ForeignKey(MedicineBrand, on_delete=models.SET_NULL, null=True)
    med_power = models.ForeignKey(MedicinePower, on_delete=models.SET_NULL, null=True)
    med_vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    buying_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    selling_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    is_out_of_stock = models.BooleanField(default=False)
    stock_amount = models.PositiveIntegerField()


    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.med_name
    
    def save(self, *args, **kwargs):
        super(Medicine, self).save(*args, **kwargs)
        if not self.med_image:
            return

    @property
    def get_medicine_by_category(self):
        return Medicine.objects.filter(
            medicinecategory__med_cat_name=self.med_name
        )
        
    @staticmethod
    def get_medicines(ids):
        return Medicine.objects.filter(
            id__in=ids
        )


class MedicineCartItems(models.Model):
    items = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
    


class MedicineCheckout(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    medicine_items = models.ManyToManyField(MedicineCartItems)
    discount = models.FloatField(null=True)
    amount_received = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    change = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)


    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return self.customer_phone