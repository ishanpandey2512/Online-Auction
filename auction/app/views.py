
from .models import Product, Buyer
from django.views import generic


class BuyerView(generic.ListView):

    template_name = 'app/buyer.html'
    context_object_name = 'product_list'

    def get_queryset(self):

        return Product.objects.order_by('id')


class ProductView(generic.DetailView):

    model = Product
    template_name = 'app/product.html'

    def __bidupdate__(self):

        if Buyer.bid_amount > Product.minimum_price:
            if Buyer.bid_amount > Product.current_bid:
                Product.current_bid = Buyer.bid_amount

        return self.Product.current_bid
