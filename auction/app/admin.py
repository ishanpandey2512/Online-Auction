from django.contrib import admin

from .models import MyProfile, Product, Bids



from django.contrib import admin

admin.site.register(MyProfile)
admin.site.register(Product)
admin.site.register(Bids)
#$('#search').keyup(function() {