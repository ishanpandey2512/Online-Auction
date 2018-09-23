
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, LoginForm, EditProfileForm

from django.contrib.auth.models import User
from django.contrib import messages

from django.views import generic

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail
from auction.settings import EMAIL_HOST_USER
from .models import MyProfile



def home(request):
    return render(request, 'home.html')

# Signup using Email Verification
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    subject = 'Your Online-Auction Email Verification is here..'
                    message = render_to_string('acc_active_email.html', {

                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode,
                        'token': account_activation_token.make_token(user),
                    })
                    from_mail = EMAIL_HOST_USER
                    to_mail = [user.email]
                    send_mail(subject, message, from_mail, to_mail, fail_silently=False)
                    messages.success(request, 'Confirm your email to complete registering with ONLINE-AUCTION.')
                    return redirect('home')
        else:
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})


#account activation function
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'EMAIL VERIFIED!!!! HURRAY....')
        return redirect('home')
    else:
        return HttpResponse('Activation Link is Invalid. Try once more...')


def logout_view(request):
    logout(request)
    messages.success(request, 'You are  logged out')
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'home.html')
            else:
                return HttpResponse('Please! Verify your Email first')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})





@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.myprofile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user.myprofile)
    return render(request, 'edit_profile.html', {'form': form})

# --------------------------------------------------------------------------------------------

# @login_required
# class VisaForm(generic.edit.FormView):
#     form_class = VisaForm
#     template_name = 'templates/visa.html'
#
#     def get(self, request, *args, **kwargs):
#         try:
#             form = self.form_class
#



from .models import Product, Bids
from django.views.generic import DetailView,FormView,ListView
from django.views.generic.edit import FormMixin
from .forms import Make_Bids


class BuyerView(ListView):

    template_name = 'app/buyer.html'
    context_object_name = 'product_list'

    def get_queryset(self):

        return Product.objects.order_by('id')


class ProductView(DetailView,FormMixin):

    model = Product
    template_name = 'app/product.html'
    # form_class = Make_Bids

    # def __bidupdate__(self):
    #     p = Product.objects.get('id')
    #     #b= Product.buy_product.objects.get(User.username)
    #
    #     if p.buy_product.bid_amount > p.minimum_price:
    #         if p.buy_product.bid_amount > p.current_bid:
    #             p.current_bid = p.buy_product.bid_amount
    #
    #     return self.p.current_bid

def add_product(request):
    if(request.method=="POST"):
        form=PostForm(request.POST)
        if form.is_valid():
            product_item=form.save(commit=False)
            product_item.save()
    else:
        form=PostForm()
    return render(request,'app/product_form.html',{'form':form})
