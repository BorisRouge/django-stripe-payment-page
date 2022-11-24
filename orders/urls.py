from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('item/<int:item_id>', views.ItemView.as_view(), name='item'),
    path('catalog', views.Catalog.as_view(), name='catalog'),
    path('create-checkout-session', views.create_checkout_session),
    path('success', views.redirect_after_transaction),
    path('cancel', views.redirect_after_transaction),
    path('', RedirectView.as_view(url='catalog')),
    ]
