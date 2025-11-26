from django.urls import path, include
from rest_framework.routers import DefaultRouter
from menu.api.viewsets import CategoryViewSet, FoodViewSet, ToppingViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'foods', FoodViewSet, basename='food')
router.register(r'toppings', ToppingViewSet, basename='topping')

urlpatterns = [
    path('', include(router.urls)),
]
