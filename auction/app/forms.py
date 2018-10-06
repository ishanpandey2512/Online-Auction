from django.core.files.images import get_image_dimensions
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyProfile, Product
from django.core.validators import MinValueValidator


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

    class Meta:
        model = MyProfile
        fields = ('avatar', 'first_name', 'last_name', 'gender', 'date_of_birth', 'phone_number')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

class VisaForm(forms.Form):
    visa_card_number = forms.CharField(max_length=16, label="Visa Number")
    exp_date = forms.DateField(widget=forms.DateInput(attrs={"placeholder":'YY/MM'}), label="Expiry Date")


class BidsForm(forms.Form):

    bidder_amount = forms.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        fields = ('bidder_amount',)


class ProductForm(forms.ModelForm):

    class Meta:


        model = Product
        fields = ('name', 'desp','category', 'minimum_price',)



