import os
from uuid import uuid4
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Item, OrderItem
from .forms import CatalogForm
import stripe


# Create your views here.

class Catalog(View):
    def get (self, request):
        print(request.user)
        context = {'items': Item.objects.all(),
                   'form': CatalogForm, }
        return render(request, template_name='orders/catalog.html', context=context,)


class ItemView(View):
    def get(self, request, item_id):
        context = {'item': Item.objects.get(pk=item_id)}
        return render(request, template_name="orders/detail.html", context=context,)


@csrf_exempt
def create_checkout_session(request):
    stripe.api_key = os.getenv('stripe_api_key')
    item = Item.objects.get(pk=request.POST.get('add'))
    session = stripe.checkout.Session.create(
        line_items=[{'price_data': {
            'product_data': {'name': item.name},
            "unit_amount": int(item.price*100),
            "currency": 'RUB'},
            "quantity": request.POST.get('quantity'),
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    return redirect(session.url, code=303)


def redirect_after_transaction(request):
    options = {'/success': 'Платеж успешно совершен.',
               '/cancel': 'Платеж отменен.', }
    return render(request,
                  template_name='orders/redirect_after_transaction.html',
                  context={'text': options[request.get_full_path()]})

# TODO: it's an 'order' or a 'cart'?
def add_to_cart(request): # TODO: checkout should deactivate the order from session
    '''Пополнение корзины.'''
    quantity = int(request.POST.get('quantity'))
    item = get_object_or_404(Item, pk=request.POST.get(f'added-item-id'))
    # Корзина привязана к сессии.
    if 'order' not in request.session.keys():
        order = Order()
        order.save()
        request.session['order'] = order.id
    active_order = Order.objects.get(pk=request.session['order'])
    # Проверяем, есть ли уже позиция в корзине.
    order_item, created = OrderItem.objects.get_or_create(item=item, order=active_order)
    if created:
        order_item.quantity += quantity
    else:
        order_item.quantity = quantity
    order_item.save()
    return redirect('catalog')



