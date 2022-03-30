from django.forms import ModelForm
from .models import Product, Brand, Store

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'quantity', 'price', 'store', 'brand', 'category', 'description', 'is_discount', 'discount_percentage']

class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['id', 'brand_name']

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'city', 'is_activ']