from django.db import models
from django.conf import settings


class Item(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)


    def __str__(self):
        return self.name


class Order(models.Model):
    pass
    # items = models.ManyToManyField(OrderItem)
    #
    # def get_total_amount(self):
    #     amount = 0
    #     for item in self.items.all():
    #         amount += item.get


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)


