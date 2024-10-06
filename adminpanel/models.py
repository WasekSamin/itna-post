from django.db import models
from SAAS.models import Shop
from restaurant.models import CountryModel



class Contact(models.Model):
    shop = models.ForeignKey(Shop, null=True, on_delete=models.SET_NULL)
    address1 = models.TextField(null=True)
    address2 = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=120, null=True)
    city = models.CharField(max_length=120, null=True)
    zip = models.CharField(max_length=120, null=True)
    country = models.ForeignKey(CountryModel, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=20, null=True)
    website = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    message = models.TextField(null=True)

    def __str__(self):
        return str(self.id)