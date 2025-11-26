from rest_framework import serializers
from menu.models import Topping




class ToppingSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Topping
        fields = [
            'id', 'name', 'description', 'price', 'final_price',
            'is_available', 'discount', 'available_from', 'available_to',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_final_price(self, obj):
        if obj.discount and obj.discount > 0:
            return round(float(obj.price) * (1 - obj.discount / 100), 2)
        return float(obj.price)
