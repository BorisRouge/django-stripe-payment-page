from django.urls import path
from . import views

urlpatterns = [
    path('', views.Item.as_view()),  # TODO: alternative names: catalogue, view, checkout.
    path('create-checkout-session', views.create_checkout_session),
    path('success', views.redirect_after_transaction),
    path('cancel', views.redirect_after_transaction),

    ]
