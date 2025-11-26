from django.test import TestCase
from django.utils import timezone
from datetime import time
from menu.models import Category, Food, FoodImage, Topping, FoodTopping
from menu.utils.availability import is_food_available
from menu.utils.pricing import calculate_final_price


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
    
    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.description, "Test Description")
        self.assertIsNotNone(self.category.created_at)
        self.assertIsNotNone(self.category.updated_at)
    
    def test_category_str(self):
        self.assertEqual(str(self.category), "Test Category")


class FoodModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.food = Food.objects.create(
            category=self.category,
            name="Test Food",
            description="Test Description",
            price=10.50
        )
    
    def test_food_creation(self):
        self.assertEqual(self.food.name, "Test Food")
        self.assertEqual(self.food.category, self.category)
        self.assertEqual(float(self.food.price), 10.50)
        self.assertTrue(self.food.is_available)
    
    def test_food_discount(self):
        self.food.discount = 20
        self.food.save()
        final_price = calculate_final_price(self.food.price, self.food.discount)
        self.assertEqual(final_price, 8.40)
    
    def test_food_time_availability(self):
        now = timezone.now().time()
        self.food.available_from = time(now.hour - 1, now.minute)
        self.food.available_to = time(now.hour + 1, now.minute)
        self.food.save()
        self.assertTrue(is_food_available(self.food))
    
    def test_food_unavailable(self):
        self.food.is_available = False
        self.food.save()
        self.assertFalse(is_food_available(self.food))


class ToppingModelTest(TestCase):
    def setUp(self):
        self.topping = Topping.objects.create(
            name="Test Topping",
            description="Test Description",
            price=2.50
        )
    
    def test_topping_creation(self):
        self.assertEqual(self.topping.name, "Test Topping")
        self.assertEqual(float(self.topping.price), 2.50)
        self.assertTrue(self.topping.is_available)
    
    def test_topping_discount(self):
        self.topping.discount = 10
        self.topping.save()
        final_price = calculate_final_price(self.topping.price, self.topping.discount)
        self.assertEqual(final_price, 2.25)


class FoodImageModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.food = Food.objects.create(
            category=self.category,
            name="Test Food",
            price=10.00
        )
    
    def test_food_image_creation(self):
        food_image = FoodImage.objects.create(food=self.food)
        self.assertEqual(food_image.food, self.food)
        self.assertIsNotNone(food_image.created_at)


class FoodToppingModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.food = Food.objects.create(
            category=self.category,
            name="Test Food",
            price=10.00
        )
        self.topping = Topping.objects.create(
            name="Test Topping",
            price=2.00
        )
    
    def test_food_topping_creation(self):
        food_topping = FoodTopping.objects.create(
            food=self.food,
            topping=self.topping
        )
        self.assertEqual(food_topping.food, self.food)
        self.assertEqual(food_topping.topping, self.topping)


class UtilsTest(TestCase):
    def test_calculate_final_price_with_discount(self):
        price = 100.00
        discount = 20
        final_price = calculate_final_price(price, discount)
        self.assertEqual(final_price, 80.00)
    
    def test_calculate_final_price_without_discount(self):
        price = 100.00
        discount = 0
        final_price = calculate_final_price(price, discount)
        self.assertEqual(final_price, 100.00)
    
    def test_is_food_available_when_available(self):
        category = Category.objects.create(name="Test Category")
        food = Food.objects.create(
            category=category,
            name="Test Food",
            price=10.00,
            is_available=True
        )
        self.assertTrue(is_food_available(food))
    
    def test_is_food_available_when_unavailable(self):
        category = Category.objects.create(name="Test Category")
        food = Food.objects.create(
            category=category,
            name="Test Food",
            price=10.00,
            is_available=False
        )
        self.assertFalse(is_food_available(food))

