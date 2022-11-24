import os
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Item, OrderItem, Discount, Tax
from .forms import CatalogForm
import stripe


# Create your views here.

class Catalog(View):
    def get (self, request):
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


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    print(item)
    order_item = OrderItem.objects.create(item_id=pk)


