from django import forms
from .models import *
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm


# # Note that password1 and password2 are part of UserCreationForm, where password2 stands for (conf.password)
# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='Required. You cant escape from it!')
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

class ContactForm(forms.ModelForm):
    userName = forms.CharField(label="Username:", widget=forms.widgets.TextInput())
    password = forms.CharField(label="Password:", min_length=6, widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput())
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'columns': 6})),
    birthDate = forms.DateTimeField(label="BirthDate :",widget=forms.DateTimeInput(attrs={'placeholder':'YYYY-MM-DD', 'type' : 'date'}))

    class Meta:
        model = Person
        fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

class SellerOrBuyer(forms.Form):
    choice_set = (('Seller', Seller), ('Buyer', Buyer))
