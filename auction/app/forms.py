
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyProfile
from django.forms.widgets import DateInput

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
             User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')


class EditProfileForm(forms.ModelForm):
     # date_of_birth = forms.DateField(widgets={ 'date_of_birth': DateInput(attrs={'type': 'date'})})
     class Meta:
         model = MyProfile
         fields=('avatar', 'first_name', 'last_name', 'gender', 'date_of_birth', 'phone_number')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password')

# class VisaForm(forms.Form):
#     # user form pre build class
# 	visaNum = forms.CharField(max_length = 10, label="Visa Number", help_text='16 Digits Required')
# 	expDate= forms.DateTimeField(label="Expiry Date:",widget=forms.DateTimeInput(attrs={'placeholder':'YYYY-MM-DD', 'type' : 'date'}))
#
#     # class Meta:
#     #     model=

from .models import Bids
from django import forms


class Make_Bids(forms.Form):
    class Meta:
        model = Bids
        field = ('bid_amount',)


