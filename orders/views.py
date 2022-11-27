import os
from uuid import uuid4
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Item, OrderItem
from .forms import CatalogForm, DetailForm
import stripe


# Create your views here.

class Catalog(View):
    def get (self, request):
        context = {'items': Item.objects.all(),
                   'form': CatalogForm, }
        return render(request, template_name='orders/catalog.html', context=context,)


class ItemView(View):
    def get(self, request, item_id):
        context = {'item': Item.objects.get(pk=item_id),
                   'form': DetailForm}
        return render(request,
                      template_name="orders/detail.html",
                      context=context,)


class CheckoutView(View):
    def get(self, request):
        active_order = Order().get_active_order(request)
        total = active_order.get_total(request)
        checkout_items = OrderItem.objects.filter(order=active_order)
        return render(request,
                      context={'checkout_items': checkout_items,
                               'total': total,
                               'active_order': {'name': active_order.name,
                                                'id': active_order.id, },
                               },
                      template_name='orders/checkout.html')


@csrf_exempt
def create_checkout_session(request):
    stripe.api_key = os.getenv('stripe_api_key')
    order_name = request.POST.get('active_order')
    total = request.POST.get('total')
    session = stripe.checkout.Session.create(
        line_items=[{'price_data': {  # TODO: parse ordered items here?
            'product_data': {'name': order_name},
            "unit_amount": int(float(total))*100,
            "currency": 'RUB'},
            "quantity": 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    return redirect(session.url, code=303)


def redirect_after_transaction(request):
    options = {'/success': 'Заказ успешно оформлен.',
               '/cancel': 'Платеж отменен.', }
    return render(request,
                  template_name='orders/redirect_after_transaction.html',
                  context={'text': options[request.get_full_path()]})

# TODO: it's an 'order' or a 'cart'?
def add_to_cart(request): # TODO: checkout should deactivate the order from session
    '''Пополнение корзины.'''
    quantity = int(request.POST.get('quantity'))
    item = get_object_or_404(Item, pk=request.POST.get(f'added-item-id'))
    active_order = Order.get_active_order(request)
    # Проверяем, есть ли уже позиция в корзине.
    order_item, created = OrderItem.objects.get_or_create(item=item, order=active_order)
    if created:
        order_item.quantity = quantity
    else:
        order_item.quantity += quantity
    order_item.save()
    return redirect('catalog')


def cancel_order(request):
    del request.session['order']
    return redirect('catalog')


