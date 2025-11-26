from django.db import models
from decimal import Decimal
from online_menu.base.models import BaseModel
from menu.mixins.models.ordering import OrderingMixin
from menu.mixins.models.__str__ import NameStrMixin, CompositeStrMixin
from menu.utils.pricing import calculate_final_price
from menu.utils.availability import is_food_available


class Category(BaseModel, NameStrMixin):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    @property
    def foods_count(self):
        return self.foods.filter(is_available=True).count()
    
    @property
    def has_icon(self):
        return bool(self.icon)

class Food(BaseModel, OrderingMixin, NameStrMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    header_image = models.ImageField(upload_to='foods/', blank=True, null=True)
    
    @property
    def final_price(self):
        return Decimal(str(calculate_final_price(self.price, self.discount)))
    
    @property
    def has_discount(self):
        return self.discount and self.discount > 0
    
    @property
    def is_currently_available(self):
        return is_food_available(self)
    
    @property
    def has_header_image(self):
        return bool(self.header_image)
    
    @property
    def discount_amount(self):
        if self.has_discount:
            return self.price - self.final_price
        return Decimal('0.00')
    
    def set_price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.price = value
    
    def set_discount(self, value):
        if value < 0 or value > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount = value

class FoodImage(BaseModel, CompositeStrMixin):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='foods/', blank=True, null=True)
    
    @property
    def has_image(self):
        return bool(self.image)

class Topping(BaseModel, OrderingMixin, NameStrMixin):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    @property
    def final_price(self):
        return Decimal(str(calculate_final_price(self.price, self.discount)))
    
    @property
    def has_discount(self):
        return self.discount and self.discount > 0
    
    @property
    def is_currently_available(self):
        from menu.utils.availability import is_food_available
        return is_food_available(self)
    
    @property
    def discount_amount(self):
        if self.has_discount:
            return self.price - self.final_price
        return Decimal('0.00')
    
    def set_price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.price = value
    
    def set_discount(self, value):
        if value < 0 or value > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount = value

class FoodTopping(BaseModel, CompositeStrMixin):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='food_toppings')
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name='food_toppings')
    
    @property
    def is_topping_available(self):
        return self.topping.is_currently_available

    class Meta:
        unique_together = ['food', 'topping']