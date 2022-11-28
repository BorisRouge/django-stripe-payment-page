import os
import requests
import stripe
from django.db import models
from datetime import datetime
from decimal import Decimal as dec
from lxml import etree




class Item(models.Model):

    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)


    def __str__(self):
        return self.name

    def get_usd(self):
        """Получает данные для перевода USD в RUB."""
        url = 'http://cbr.ru/scripts/XML_daily.asp'
        response = requests.get(url)
        response.raise_for_status()
        content = response.content
        root = etree.fromstring(content)
        valute = "//Valute[@ID='R01235']/Value/text()"
        # Берем котировку USD, меняем десятичный разделитель, преобразуем в Decimal для расчетов.
        usd = dec(str(root.xpath(valute)[0]).replace(',','.'))
        price_usd = self.price/usd
        return round(price_usd, 2)

class Order(models.Model):  # TODO: Дать имена Order и Item.
    name = models.CharField(max_length=55, null=True)
    total = models.DecimalField(max_digits=40, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def create(request): #TODO: А не использовать ли просто Order(name=)
        order = Order()
        order.name = f'Заказ {request.user} ' \
                     f'от {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        order.save()
        return order

    @staticmethod
    def get_active_order(request):
        '''Привязка корзины к сессии.'''
        if 'order' not in request.session.keys():
            order = Order.create(request) #TODO: А не использовать ли просто Order(name=)
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
               f'на сумму: {self.get_amount()} RUB'

    def get_amount(self):
        return self.item.price*self.quantity


class Discount(models.Model):
    name = models.CharField(max_length=55, blank=False)
    stripe_id = models.CharField(max_length=55, default='Automatically assigned')
    promocode = models.CharField(max_length=55, blank=False)
    percent_off = models.IntegerField(blank=False)
    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super(Discount, self).save(*args, **kwargs)
        self.stripify()

    def stripify(self):
        stripe.api_key = os.getenv('stripe_api_key')
        coupon = stripe.Coupon.create(name=self.name,
                                      percent_off=self.percent_off,)
        stripe.PromotionCode.create(coupon=coupon.id, code=self.promocode)
        self.stripe_id = coupon.id
        print(f'Stripified, stripe_id: {self.stripe_id}, coupon_id: {coupon.id}')
        return coupon

    @staticmethod
    def visible_in_checkout():
        visible_discount = Discount.objects.filter(
            active=True,
            visible=True).last()
        return visible_discount

