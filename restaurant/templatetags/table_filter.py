from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name="cart_quantity")
def cart_quantity(item_id, cart2):
    keys = cart2.keys()
    for id in keys:
        if int(id) == item_id.id:
            return cart2.get(id)
    return False


@register.filter(name="cart_total")
def cart_total(item_id, cart2):
    return item_id.item_price * cart_quantity(item_id, cart)



@register.filter(name="get_grand_total")
def get_grand_total(items, cart2):
    total = 0
    for i in items:
        total += cart_total(i, cart2)
    return total