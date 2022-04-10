from django.contrib import admin
from .models import Product, Brand, Category, Store, ProductColor, ProductSize, Orders, Company

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'quantity', 'category', 'store', 'description', 'price', 'brand', 'color', 'size', 'is_discount', 'discount_percentage', 'created_by', 'modified_by', 'created_at', 'updated_at']
    fields = ['id', 'product_name', 'quantity', 'category', 'store', 'description', 'price', 'brand', 'color', 'size', 'is_discount', 'discount_percentage', 'created_by', 'modified_by', 'created_at', 'updated_at']
    readonly_fields = ('id','created_at', 'updated_at', 'created_by', 'modified_by')

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
    fields = ('name', 'parent')

    class Meta:
        model = Category

    def get_queryset(self, request):
        return Category.objects.all()

admin.site.register(Category, CategoryAdmin)


class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'city', 'is_activ']
    fields = ('store_name', 'city', 'is_activ')

    class Meta:
        model = Store

admin.site.register(Store, StoreAdmin)


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['color', 'color_code']
    fields = ('color', 'color_code')

    class Meta:
        model = ProductColor

admin.site.register(ProductColor, ProductColorAdmin)


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    fields = ('size',)

    class Meta:
        model = ProductSize

admin.site.register(ProductSize, ProductSizeAdmin)


class OrdersAdmin(admin.ModelAdmin):
    list_display = [
        'user'
        ,'product'
        ,'quantity'
        ,'status'
        ,'vat'
        ,'discount'
        ,'company'
        ,'shipping'
        ,'gross_amount'
        ,'net_amount'
        ,'info_order'
        ,'created_at'
        ,'updated_at'
    ]
    fields = (
        'user'
        ,'product'
        ,'quantity'
        ,'status'
        ,'vat'
        ,'discount'
        ,'company'
        ,'shipping'
        ,'gross_amount'
        ,'net_amount'
        ,'info_order'
        ,'created_at'
        ,'updated_at'
    )
    readonly_fields = ('created_at', 'updated_at', 'gross_amount', 'net_amount')
    class Meta:
        model = Orders

admin.site.register(Orders, OrdersAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'name'
        ,'country'
        ,'city'
        ,'address'
        ,'phone'
    ]
    
    fields = (
        'name'
        ,'country'
        ,'city'
        ,'address'
        ,'phone'
    )

    class Meta:
        model = Company

admin.site.register(Company, CompanyAdmin)