from django.shortcuts import render
from django.views import View

# Create your views here.


class Item(View):  # TODO: see todo in urls.
    def get(self, request):
        return render(request, template_name="orders/page.html")