import os
import sys
import django

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()
# Import your models
from crm.models import Customer, Product

# Seed data
customers = [
    {"name": "Alice", "email": "alice@example.com", "phone": "+1234567890"},
    {"name": "Bob", "email": "bob@example.com", "phone": "123-456-7890"},
    {"name": "Carol", "email": "carol@example.com", "phone": None},
]

products = [
    {"name": "Laptop", "price": 999.99, "stock": 10},
    {"name": "Phone", "price": 499.99, "stock": 20},
    {"name": "Headphones", "price": 149.99, "stock": 15},
]

# Create or get customers
for c in customers:
    Customer.objects.get_or_create(
        name=c["name"], email=c["email"], phone=c["phone"]
    )

# Create or get products
for p in products:
    Product.objects.get_or_create(
        name=p["name"], price=p["price"], stock=p["stock"]
    )

print("Database seeded successfully.")
