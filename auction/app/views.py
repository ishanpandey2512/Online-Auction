from django.http import HttpResponse
from .models import Product
from django.views import generic


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class ProductView(generic.DetailView):

    model = Product
    template_name = 'app/product.html'