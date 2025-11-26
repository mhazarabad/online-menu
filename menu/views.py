from django.shortcuts import render, get_object_or_404
from menu.models import Category, Food
from menu.utils.availability import is_food_available
from menu.utils.pricing import calculate_final_price
from menu.constants.templates import (
    MENU_TEMPLATE, 
    FOOD_DETAIL_TEMPLATE
)

def menu_list(request):
    categories = Category.objects.prefetch_related(
        'foods__images',
        'foods__food_toppings__topping',
    ).all()
    
    menu_data = []
    for category in categories:
        foods = []
        for food in category.foods.all():
            if is_food_available(food):
                final_price = calculate_final_price(food.price, food.discount)
                foods.append({
                    'food': food,
                    'final_price': final_price,
                    'has_discount': food.discount and food.discount > 0,
                })
        
        if foods:
            menu_data.append({
                'category': category,
                'foods': foods,
            })
    
    context = {
        'menu_data': menu_data,
    }
    return render(request, MENU_TEMPLATE, context)

def food_detail(request, food_id):
    food = get_object_or_404(
        Food.objects.prefetch_related('images', 'food_toppings__topping'),
        id=food_id
    )
    
    is_available = is_food_available(food)
    final_price = calculate_final_price(food.price, food.discount)
    has_discount = food.discount and food.discount > 0
    
    available_toppings = []
    for food_topping in food.food_toppings.all():
        topping = food_topping.topping
        if topping.is_available:
            topping_final_price = calculate_final_price(topping.price, topping.discount)
            available_toppings.append({
                'topping': topping,
                'final_price': topping_final_price,
                'has_discount': topping.discount and topping.discount > 0,
            })
    
    context = {
        'food': food,
        'is_available': is_available,
        'final_price': final_price,
        'has_discount': has_discount,
        'available_toppings': available_toppings,
        'images': food.images.all(),
    }
    return render(request, FOOD_DETAIL_TEMPLATE, context)
