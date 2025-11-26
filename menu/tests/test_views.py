from django.test import TestCase, Client
from django.urls import reverse
from menu.models import Category, Food, Topping, FoodTopping


class MenuListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        self.food = Food.objects.create(
            category=self.category,
            name="Test Food",
            description="Test Description",
            price=10.00,
            is_available=True
        )
    
    def test_menu_list_view(self):
        response = self.client.get(reverse('menu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")
        self.assertContains(response, "Test Food")
    
    def test_menu_list_view_with_unavailable_food(self):
        self.food.is_available = False
        self.food.save()
        response = self.client.get(reverse('menu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Food")
    
    def test_menu_list_empty(self):
        Food.objects.all().delete()
        Category.objects.all().delete()
        response = self.client.get(reverse('menu_list'))
        self.assertEqual(response.status_code, 200)


class FoodDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.food = Food.objects.create(
            category=self.category,
            name="Test Food",
            description="Test Description",
            price=10.00,
            is_available=True
        )
    
    def test_food_detail_view(self):
        response = self.client.get(reverse('food_detail', args=[self.food.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Food")
        self.assertContains(response, "Test Description")
        self.assertContains(response, "€10.00")
    
    def test_food_detail_view_not_found(self):
        response = self.client.get(reverse('food_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
    
    def test_food_detail_with_discount(self):
        self.food.discount = 20
        self.food.save()
        response = self.client.get(reverse('food_detail', args=[self.food.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "-20")
    
    def test_food_detail_with_toppings(self):
        topping = Topping.objects.create(
            name="Test Topping",
            price=2.00,
            is_available=True
        )
        FoodTopping.objects.create(
            food=self.food,
            topping=topping
        )
        response = self.client.get(reverse('food_detail', args=[self.food.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Topping")

