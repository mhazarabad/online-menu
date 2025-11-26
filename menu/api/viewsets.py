from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from menu.models import Category, Food, Topping
from menu.serializers import (
    CategorySerializer,
    FoodSerializer,
    FoodDetailSerializer,
    ToppingSerializer,
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class FoodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Food.objects.select_related('category').prefetch_related('images', 'food_toppings__topping')
    serializer_class = FoodSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        available_only = self.request.query_params.get('available_only', 'true')
        
        if category:
            queryset = queryset.filter(category_id=category)
        
        if available_only.lower() == 'true':
            queryset = self._filter_by_availability(queryset)
        
        return queryset
    
    def _filter_by_availability(self, queryset):
        now = timezone.now().time()
        return queryset.filter(
            is_available=True
        ).filter(
            Q(available_from__isnull=True, available_to__isnull=True) |
            Q(available_from__lte=now, available_to__gte=now) |
            Q(available_from__lte=now, available_to__isnull=True) |
            Q(available_from__isnull=True, available_to__gte=now)
        )
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FoodDetailSerializer
        return FoodSerializer
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({'error': 'category_id parameter is required'}, status=400)
        
        queryset = self.get_queryset().filter(category_id=category_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ToppingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        available_only = self.request.query_params.get('available_only', 'true')
        
        if available_only.lower() == 'true':
            now = timezone.now().time()
            queryset = queryset.filter(
                is_available=True
            ).filter(
                Q(available_from__isnull=True, available_to__isnull=True) |
                Q(available_from__lte=now, available_to__gte=now) |
                Q(available_from__lte=now, available_to__isnull=True) |
                Q(available_from__isnull=True, available_to__gte=now)
            )
        
        return queryset
