from django.contrib import admin
from .models import Product  # Replace with your model name

admin.site.register(Product)  # Register your models to be accessible in the admin interface
