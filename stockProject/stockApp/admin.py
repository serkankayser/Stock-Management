from django.contrib import admin
from .models import Product, Brand, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name']
    fields = ['id', 'product_name', 'quantity', 'category', 'description', 'price', 'brand', 'is_discount', 'discount_percentage', 'created_at', 'updated_at']
    readonly_fields = ('id','created_at', 'updated_at',)

    class Meta:
        model = Product

    def get_queryset(self, request):
        return Product.objects.all()

admin.site.register(Product, ProductAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand_name']
    fields = ['brand_name']

    class Meta:
        model = Brand

    def get_queryset(self, request):
        return Brand.objects.all()

admin.site.register(Brand, BrandAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug']
    fields = ('name', 'parent', 'slug')

    class Meta:
        model = Category

    def get_queryset(self, request):
        return Category.objects.all()

admin.site.register(Category, CategoryAdmin)