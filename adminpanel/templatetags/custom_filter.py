from django import template
from decimal import Decimal
from django.db.models import Sum, Avg
register = template.Library()


@register.filter(name="total_transaction")
def total_transaction(queryset):
    return Sum(queryset.grand_total)