from django.db import models
from datetime import datetime
from django.conf import settings


class Item(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)


    def __str__(self):
        return self.name


class Order(models.Model):  # TODO: Дать имена Order и Item.
    name = models.CharField(max_length=55, null=True)
    total = models.DecimalField(max_digits=40, decimal_places=2, default=0)


    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def create(request):
        order = Order()
        order.name = f'Заказ {request.user} ' \
                     f'от {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        order.save()
        return order

    @staticmethod
    def get_active_order(request):
        '''Привязка корзины к сессии.'''
        if 'order' not in request.session.keys():
            order = Order.create(request)
            request.session['order'] = order.id
            print(order.id)
        return Order.objects.get(pk=request.session['order'])

    @staticmethod
    def get_total(request):
        active_order = Order().get_active_order(request)
        checkout_items = OrderItem.objects.filter(order=active_order)
        total = 0
        for item in checkout_items:
            total += item.get_amount()
        return total



class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.item.name}'

    def checkout_view(self):
        return f'{self.item.name}, ' \
               f'количество: {self.quantity}, ' \
               f'на сумму: {self.get_amount()}'

    def get_amount(self):
        return self.item.price*self.quantity



