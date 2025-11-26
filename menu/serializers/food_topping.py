from rest_framework import serializers
from menu.models import FoodTopping
from menu.serializers.topping import ToppingSerializer



class FoodToppingSerializer(serializers.ModelSerializer):
    topping = ToppingSerializer(read_only=True)
    topping_id = serializers.IntegerField(write_only=True, required=True)
    
    class Meta:
        model = FoodTopping
        fields = ['id', 'food', 'topping', 'topping_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
