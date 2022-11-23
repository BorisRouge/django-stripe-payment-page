from django.urls import path
from . import views

urlpatterns = [
    path('', views.Item.as_view(), name='orders'),  # TODO: alternative names: catalogue, view, checkout.
]
