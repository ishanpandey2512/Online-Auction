
from .models import Product, Bids
from django.views.generic import DetailView,FormView,ListView
from django.views.generic.edit import FormMixin
from .forms import Make_Bids


class BuyerView(ListView):

    template_name = 'app/buyer.html'
    context_object_name = 'product_list'

    def get_queryset(self):

        return Product.objects.order_by('id')


class ProductView(DetailView,FormMixin):

    model = Product
    template_name = 'app/product.html'
    # form_class = Make_Bids

    # def __bidupdate__(self):
    #     p = Product.objects.get('id')
    #     #b= Product.buy_product.objects.get(User.username)
    #
    #     if p.buy_product.bid_amount > p.minimum_price:
    #         if p.buy_product.bid_amount > p.current_bid:
    #             p.current_bid = p.buy_product.bid_amount
    #
    #     return self.p.current_bid
