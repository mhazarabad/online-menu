from rest_framework import serializers
from menu.models import Food, FoodImage
from menu.serializers.category import CategorySerializer
from menu.serializers.food_topping import FoodToppingSerializer



class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields = ['id', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class FoodSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=True)
    final_price = serializers.SerializerMethodField()
    images = FoodImageSerializer(many=True, read_only=True)
    toppings = serializers.SerializerMethodField()
    
    class Meta:
        model = Food
        fields = [
            'id', 'category', 'category_id', 'name', 'description', 'price',
            'final_price', 'header_image', 'images', 'toppings',
            'is_available', 'discount', 'available_from', 'available_to',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_final_price(self, obj):
        if obj.discount and obj.discount > 0:
            return round(float(obj.price) * (1 - obj.discount / 100), 2)
        return float(obj.price)
    
    def get_toppings(self, obj):
        available_toppings = obj.food_toppings.filter(topping__is_available=True)
        return FoodToppingSerializer(available_toppings, many=True).data

class FoodDetailSerializer(FoodSerializer):
    all_toppings = serializers.SerializerMethodField()
    
    class Meta(FoodSerializer.Meta):
        fields = FoodSerializer.Meta.fields + ['all_toppings']
    
    def get_all_toppings(self, obj):
        return FoodToppingSerializer(obj.food_toppings.all(), many=True).data
