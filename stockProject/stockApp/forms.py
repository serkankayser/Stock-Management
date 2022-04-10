from django.forms import ModelForm
from .models import Product, Brand, Store, Category, Orders

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'quantity', 'price', 'store', 'brand', 'color', 'size', 'category', 'description', 'is_discount', 'discount_percentage']

class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['id', 'brand_name']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'city', 'is_activ']

class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['user','product','quantity','status','vat','discount','company','shipping','info_order']