from django.db import models

from core.models import TimeStampModel

class Status(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'statuses'

class Cart(TimeStampModel):
    quantity = models.IntegerField()
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    option   = models.ForeignKey('products.Option', on_delete=models.CASCADE)

    class Meta:
        db_table = 'carts'

class Order(TimeStampModel):
    order_number = models.CharField(max_length=100)
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status       = models.ForeignKey('Status', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OrderItem(TimeStampModel):
    quantity = models.IntegerField()
    product  = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order    = models.ForeignKey('Order', on_delete=models.CASCADE)
    status   = models.ForeignKey('Status', on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_items'