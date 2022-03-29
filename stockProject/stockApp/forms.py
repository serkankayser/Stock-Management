from django.forms import ModelForm
from .models import Product, Brand

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'quantity', 'price', 'brand', 'category', 'description', 'is_discount', 'discount_percentage']

class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['id', 'brand_name']
