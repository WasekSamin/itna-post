from django.contrib import admin
from restaurant.models import *
from .models import Contact
# Register your models here.


admin.site.register([
    CountryModel,
    CityModel,
    Contact
])