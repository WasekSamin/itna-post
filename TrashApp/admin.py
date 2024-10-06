from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register([
    RolesTrashModel,
    EmployeeTrashModel,
    SellingSessionTrashModel,
    CustomerTrashModel,
    VendorTrashModel,
    BrandTrashModel,
    CategoryTrashModel,
    ItemTrashModel,
    TableTrashModel,
    RestCheckoutTrashModel,
    DueTrashModel,
    RefundTrashModel,
    AdvanceBookingTrashModel,
    
])