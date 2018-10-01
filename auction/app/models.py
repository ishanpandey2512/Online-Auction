
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


class Visa(models.Model):
    userid = models.ForeignKey(MyProfile, on_delete=models.CASCADE)
    visaNum = models.CharField(max_length=16)
    expDate = models.DateField()


class Product(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, related_name='%(class)s_seller')
    name = models.CharField(max_length=50, blank=False)
    desp = models.TextField(max_length=500, blank=False, null=True)
    image = models.ImageField(upload_to='../static/images/', blank=True, null=True)
    category = models.CharField(max_length=50, blank=True,null=True)
    minimum_price = models.IntegerField(blank=True, validators=[MinValueValidator(1)],default=1)
    start = models.DateTimeField(default=timezone.now, null=True)
    end_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=1))
    current_bid = models.IntegerField(default=0)
    product_sold = models.BooleanField(default=False)
    bidder_id = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_bidder')


    def __str__(self):
        return str(self.id)

    # def getimage(instance, filename):
    #     return "static/images/image_{0}_{1}".format(str(time()), filename)

#
# class Bids(models.Model):
#     bidder_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     bid_amount = models.IntegerField(validators=[MinValueValidator(1)], default=0, null=True)
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

