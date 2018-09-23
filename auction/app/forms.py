from .models import Bids
from django import forms


class Make_Bids(forms.Form):
    class Meta:
        model = Bids
        field = ('bid_amount',)

