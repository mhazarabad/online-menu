from django import template
from menu.utils.availability import is_food_available
from menu.utils.pricing import calculate_final_price

register = template.Library()


@register.filter
def final_price(price, discount):
    return calculate_final_price(price, discount)

@register.filter
def has_discount(discount):
    return discount and discount > 0

@register.filter
def is_available(food):
    return is_food_available(food)

@register.filter
def format_price(price):
    return f"€{price:.2f}"

@register.filter
def format_discount(discount):
    if discount and discount > 0:
        return f"-{discount}%"
    return ""