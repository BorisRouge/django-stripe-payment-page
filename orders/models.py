from django.db import models


class Order(models.Model):
    pass


class Item(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount = models.IntegerField()
    tax = models.IntegerField()
    final_price = models.DecimalField(max_digits=20, decimal_places=2)


class Discount(models.Model):
    pass


class Tax(models.Model):
    pass