from rest_framework import serializers
from menu.models import Category




class CategorySerializer(serializers.ModelSerializer):
    foods_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'foods_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_foods_count(self, obj):
        return obj.foods.filter(is_available=True).count()
