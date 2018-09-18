from django.http import HttpResponse
from .models import Product
from django.views import generic


class BuyerView(generic.ListView):

    template_name = 'app/buyer.html'
    context_object_name = 'product_list'

    def get_queryset(self):

        return Product.objects.order_by('name')




class ProductView(generic.DetailView):

    model = Product
    template_name = 'app/product.html'