
import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from time import time


class MyProfile(models.Model):

    CHOICE_SET1 = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True,null=True)
    last_name = models.CharField(max_length=100, blank=True,null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(max_length=10, null=True, blank=True)
    avatar = models.ImageField(upload_to='profile_pic', default='profile.png')
    gender = models.CharField(max_length=10, choices=CHOICE_SET1, default='Male')

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_MyProfile(sender, instance, created, **kwargs):
        if created:
            MyProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_MyProfile(sender, instance, **kwargs):
        instance.myprofile.save()

# class Visa(models.Model):
# 	userid =models.ForeignKey(MyProfile, on_delete=models.CASCADE)
# 	visaNum = models.CharField(max_length = 16)
# 	expDate=models.DateTimeField()
#     def __str__(self):
#         return str(self.id)



class Product(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    desp = models.TextField(max_length=500, blank=False, null=True)
    image = models.ImageField(upload_to='../static/images/', blank=True, null=True)
    category = models.CharField(max_length=50, blank=True,null=True)
    minimum_price = models.IntegerField(blank=True, validators=[MinValueValidator(1)],default=1)
    start = models.DateTimeField(default=timezone.now, null=True)
    end_date = models.DateTimeField(default=datetime.date.today() + datetime.timedelta(days=1))
    current_bid = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    def getimage(instance, filename):
         return "static/images/image_{0}_{1}".format(str(time()), filename)

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.IntegerField(validators=[MinValueValidator(1)], default=0,  null=True)
    buy_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

# class Bidsmade(models.Model):
#
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     bidder_name = models.CharField(max_length=30, blank=False)
#     bid_time = models.TimeField(timezone.now())
#     bid_amount = models.DecimalField(max_digits=10,decimal_places=2)
#
#     def __str__(self):
#         return self.product.name



# class seller(models.Model):
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.name


# class product(models.Model):
#     choice_of_category = (("Jwellery", "Jwellery"), ("Clothes", "Clothes"), ("fruits", "fruits"),
#                           ("crocery", "crocery"), ("footwear", "footwear"),)
#
#     user1 = models.ForeignKey(seller, on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=100, null=True)
#     image = models.ImageField(upload_to="images", default='static/images/apple.jpg')
#     category = models.CharField(max_length=20, choices=choice_of_category, null=True)
#     description = models.TextField(max_length=300, null=True)
#     minimum_price = models.DecimalField(max_digits=10, decimal_places=2)
#
#     created = models.DateTimeField('created', auto_now_add=True)
#     '''
#     price = models.PositiveSmallIntegerField(default=0)
#
#     modified = models.DateTimeField('modified',auto_now=True)'''
#
#     def __str__(self):
#         return str(self.product_name)
