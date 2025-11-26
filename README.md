# Online Menu System

An online menu system built with Django tempaltes and Django REST Framework. Perfect for restaurants, cafes, and food establishments looking to showcase their menu digitally with a responsive interface and a API for frontend integration.

![Demo](demo/template.gif)

## Features

### Core Functionality
- Category-based Menu Organization - Organize foods by categories with custom icons
- Food Details - Each food item includes descriptions, multiple images, and pricing
- Topping System - Flexible topping management with individual pricing
- Discount Management - Apply percentage-based discounts to foods and toppings
- Time-based Availability - Set specific time windows when items are available
- Availability Status - Mark items as available/unavailable with visual indicators

### User Interface
- Responsive Design - Seamlessly works on desktop, tablet, and mobile devices
- Modern & Minimal UI - Clean, animated interface with smooth transitions
- Image Gallery - Interactive image slider with modal view for food details
- Real-time Pricing - Automatic calculation and display of discounted prices
- Visual Badges - Clear indicators for discounts and availability status
- Euro Currency - All prices displayed in Euro (€)
- Separated Assets - HTML, CSS, and JavaScript files are properly separated

### API & Integration
- RESTful API - Complete REST API built with Django REST Framework
- Swagger Documentation - Interactive API documentation with Swagger UI
- Advanced Filtering - Filter by category, availability, search by name/description
- Pagination - Efficient pagination for large datasets
- CORS Enabled - Ready for frontend integration

![Demo](demo/swagger.gif)

### Admin Panel
- Customized Admin Interface - Enhanced Django admin with image previews
- Rich Display - Visual indicators for discounts, availability, and pricing
- Inline Editing - Manage food images and toppings directly from food pages
- Comprehensive Filtering - Filter and search across all models

![Demo](demo/admin.gif)

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd online-menu
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create superuser (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. Collect static files
   ```bash
   python manage.py collectstatic
   ```

7. Run development server
   ```bash
   python manage.py runserver
   ```

8. Access the application
   - Web Interface: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Documentation: http://127.0.0.1:8000/swagger/
   - ReDoc Documentation: http://127.0.0.1:8000/redoc/

## Testing

Run the comprehensive test suite:

```bash
python manage.py test
```

The test suite includes:
- Model tests (creation, relationships, business logic, properties)
- View tests (template rendering, context data)
- API tests (endpoints, serialization, filtering)
- Utility function tests

## License

This project is part of a portfolio and is available for educational purposes.

