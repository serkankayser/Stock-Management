from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from cities_light.models import City, Region
from decimal import Decimal
from django.utils.text import slugify
from auditlog.registry import auditlog


class Brand(models.Model):
    brand_name = models.CharField(max_length=50)

    def __str__(self):
        return self.brand_name

exclude = ['created_by', 'modified_by']

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(
        'Category',
        related_name="prod_category",
        on_delete=models.CASCADE)
    store = models.ForeignKey(
        'Store',
        related_name="prod_store",
        on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=0)
    color = models.ForeignKey('ProductColor', on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey('ProductSize', on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_%(class)s_set', null=False, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_%(class)s_set', null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    @property
    def discount(self):
        if self.is_discount:
            self.sale_price = round(Decimal(self.price - self.price * self.discount_percentage / 100),2)
            return self.sale_price


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"   

    def __str__(self):                           
        full_path = [self.name]            
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])


class Store(models.Model):
    store_name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    is_activ = models.BooleanField(default=True)

    def __str__(self):
        return self.store_name


class ProductSize(models.Model):
    size=models.CharField(max_length=100)

    def __str__(self):
        return self.size


class ProductColor(models.Model):
    color=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    def __str__(self):
        return self.color


auditlog.register(Product)