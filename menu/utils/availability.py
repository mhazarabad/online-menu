from django.utils import timezone

def is_food_available(food):
    if not food.is_available:
        return False
    if food.available_from is not None and food.available_from>timezone.now().time():
        return False
    if food.available_to is not None and food.available_to<timezone.now().time():
        return False
    return True