from django.utils import timezone


def is_food_available(food):
    if not food.is_available:
        return False
    
    if food.available_from is None and food.available_to is None:
        return True
    
    now = timezone.now().time()
    
    if food.available_from and food.available_to:
        if food.available_from <= food.available_to:
            return food.available_from <= now <= food.available_to
        else:
            return now >= food.available_from or now <= food.available_to
    
    if food.available_from:
        return now >= food.available_from
    
    if food.available_to:
        return now <= food.available_to
    
    return True
