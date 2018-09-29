from django.core.validators import MinValueValidator
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyProfile, Product, Bids

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

'''
class Make_Bids(forms.Form):
    class Meta:
        model = Bids
        field = ('bid_amount',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'desp', 'image', 'category', 'minimum_price',)'''

class BidsForm(forms.Form):

    bidder_amount = forms.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        fields = ('bid_amount',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'desp', 'image', 'category', 'minimum_price',)


'''
class categoryForm(forms.ModelForm):

    class Meta:
        widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

        model = Product
        fields=('name')
'''