from django.db import models

from core.models import TimeStampModel

class Category(models.Model):
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    class Meta:
        db_table = 'categories'

class Product(TimeStampModel):
    name     = models.CharField(max_length=100)
    price    = models.DecimalField(max_digits=15, decimal_places=2)
    is_green = models.BooleanField(default=False)
    is_best  = models.BooleanField(default=False)
    stock    = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

class ProductImage(models.Model):
    url     = models.CharField(max_length=200)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'

class Option(models.Model):
    name    = models.CharField(max_length=50)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'options'