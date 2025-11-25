from django.db import models
from online_menu.base.models import BaseModel
from menu.mixins.models.ordering import OrderingMixin

class Category(BaseModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)

class Food(BaseModel, OrderingMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    header_image = models.ImageField(upload_to='foods/', blank=True, null=True)

class FoodImage(BaseModel):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='foods/', blank=True, null=True)

class Topping(BaseModel, OrderingMixin):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class FoodTopping(BaseModel):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='food_toppings')
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name='food_toppings')