from django.contrib import admin

from .models import MyProfile, Product, Bids

admin.site.register(MyProfile)
admin.site.register(Product)
admin.site.register(Bids)
