from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(
    [
        Vendor,
        Brand,
        Category,
        SellingType,
        Item,
        Table,
        TableItems,
        CartItems,
        TableCheckout,
        RestCheckout,
        Customer,
        DueModel,
        RefundModel,
        AdvanceBookingModel,
        SellingSession,
        Employee,
        Roles
    ]
)