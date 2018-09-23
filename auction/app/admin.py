from django.contrib import admin

from .models import MyProfile



from django.contrib import admin
from .models import seller,product
admin.site.register(MyProfile)
admin.site.register(seller)
admin.site.register(product)
