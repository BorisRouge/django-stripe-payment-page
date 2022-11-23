import os
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import stripe


# Create your views here.


class Item(View):  # TODO: see todo in urls.
    def get(self, request):
        return render(request, template_name="orders/page.html")


@csrf_exempt
def create_checkout_session(request):
    stripe.api_key = os.getenv('stripe_api_key')
    session = stripe.checkout.Session.create(
        line_items=[{'price_data': {
            'product_data': {'name': 'employee'},
            "unit_amount": f"{request.POST.get('item_1')}",
            "currency": 'RUB'},
            "quantity": 1,
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


