from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from menu.models import Category, Food, Topping








class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        self.food = Food.objects.create(
            category=self.category,
            name="Test Food",
            price=10.00,
            is_available=True
        )
    
    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Test Category")
    
    def test_retrieve_category(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Category")
    
    def test_category_foods_count(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['foods_count'], 1)

class FoodAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")
        self.food = Food.objects.create(
            category=self.category,
            name="Test Food",
            description="Test Description",
            price=10.00,
            is_available=True
        )
    
    def test_list_foods(self):
        url = reverse('food-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Test Food")
    
    def test_retrieve_food(self):
        url = reverse('food-detail', args=[self.food.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Food")
        self.assertEqual(float(response.data['price']), 10.00)
    
    def test_food_final_price_with_discount(self):
        self.food.discount = 20
        self.food.save()
        url = reverse('food-detail', args=[self.food.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['final_price'], 8.00)
    
    def test_food_filter_by_category(self):
        url = reverse('food-list')
        response = self.client.get(url, {'category': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(data), 1)
    
    def test_food_search(self):
        url = reverse('food-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(data), 1)
    
    def test_food_by_category_action(self):
        url = reverse('food-by-category')
        response = self.client.get(url, {'category_id': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class ToppingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.topping = Topping.objects.create(
            name="Test Topping",
            description="Test Description",
            price=2.50,
            is_available=True
        )
    
    def test_list_toppings(self):
        url = reverse('topping-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Test Topping")
    
    def test_retrieve_topping(self):
        url = reverse('topping-detail', args=[self.topping.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Topping")
        self.assertEqual(float(response.data['price']), 2.50)
    
    def test_topping_final_price_with_discount(self):
        self.topping.discount = 10
        self.topping.save()
        url = reverse('topping-detail', args=[self.topping.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['final_price'], 2.25)
