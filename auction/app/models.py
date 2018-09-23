import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

# functions to be used inside models are declared above
#profile_imagefile_name assigns a unique imagename/id to the uploaded image.

# def profile_imagefile_name(instance, filename):
#     ext = filename.split('.')[-1]
#     filename = "%s.%s" % (uuid.uuid4(), ext)
#     return os.path.join('profile_pic', filename)

    # ext = filename.split('.')[-1]
    # filename = "%s_%s.%s" % (instance..userid.id, instance., ext)
    # return '/'.join(['app/static/app/images', filename])

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


