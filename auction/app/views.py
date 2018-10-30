from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import SignupForm, LoginForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail
from auction.settings import EMAIL_HOST_USER
from .forms import ProductForm
from .models import Product
from .forms import BidsForm
from django.views import View


# ---------------------------HOME PAGE --------------------------------------------------------------------------------

class Home(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'app/home.html')


# -----------------AJAX SEARCH BAR CODE--------------------------------------------------------------------------------


def search(request):
    text = request.GET.get("value", "")
    product = Product.objects.filter(category__iexact=text).values_list('name', 'id')

    data = {}
    data['products'] = list(product)

    return JsonResponse(data)


# ---------------------SIGN UP CODE-------------------------------------------------------------------------


class SignUp(View):
    form = SignupForm()

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Your Online-Auction Email Verification is here..'
            message = render_to_string('app/acc_active_email.html', {

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
            return render(request, 'app/signup.html', {'form': form})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = SignupForm()
            return render(request, 'app/signup.html', {'form': form})


# -----------------------VERIFYING USER CODE------------------------------------------------------------------------


class Activate(View):

     def get(self, request, token, uidb64):

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
            messages.error(request, "Activation Email Link is Invalid.Please try again!!")
            return redirect('home')


# -----------------LOGOUT CODE------------------------------------------------------------------------------------------


class LogoutView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been successfully Logged Out!!')
        return redirect('home')


# -------------LOGIN CODE----------------------------------------------------------------------------


class LoginView(View):

    def post(self, request, *args, **kwargs):
        # form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'app/home.html')
            else:
                return HttpResponse('Please! Verify your Email first')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')

    def get(self, request, *args, **kwagrs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = LoginForm()
        return render(request, 'app/login.html', {'form': form})


# ---------------------USER CAN VIEW HIS/HER PROFILE--------------------------------------------------------------------


class ProfileView(View):

    @method_decorator(login_required)
    def get(self, request, user_id, *args, **kwargs):
        user_object = User.objects.get(id=user_id)
        context = {
            "user": user_object
        }
        return render(request, 'app/profile.html', context)


#  -----------------------USER CAN EDIT HIS/HER PROFILE-----------------------------------------------------------------


class ProfileEdit(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user_obj = request.user.id
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.myprofile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_obj)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = EditProfileForm(instance=request.user.myprofile)
        context = {
            "form": form,
        }
        return render(request, 'app/edit_profile.html', context)


#  ---------------SELLER ADDS PRODUCT FOR BIDDING-----------------------------------------------------------------------


class AddProduct(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        if form.is_valid():
            product_item = form.save(commit=False)
            product_item.seller_id = request.user
            product_item.save()
            return redirect('home')

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = ProductForm()
        context = {'form' : form}
        return render(request, 'app/product_form.html', context)


# -------------------------------BUYER CAN SEE ALL THE LISTED PRODUCTS AND SORT THEM ACCORDINGLY------------------------

class BuyerView(View):

    template_name = 'app/buyer.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {
            'product_list': Product.objects.order_by('id'),
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        sort_by = request.POST['sort']
        if sort_by == 'new_to_old':
            context = {
                'product_list': Product.objects.order_by('-start'),
            }

        elif sort_by == 'old_to_new':
            context = {
                'product_list': Product.objects.order_by('start'),
            }

        elif sort_by == 'high_to_low':
            context = {
                'product_list': Product.objects.order_by('-current_bid'),
            }

        elif sort_by == 'low_to_high':
            context = {
                'product_list': Product.objects.order_by('current_bid'),
            }

        elif sort_by == 'unsold':
            context = {
                'product_list': Product.objects.filter(product_sold='False').order_by('?'),
            }

        return render(request, self.template_name, context)


# --------------------------USER CAN SEE DETAILS OF A PARTICULAR PRODUCT AND CAN BID------------------------------------

class ProductView(View):

    template_name = 'app/product.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        time_now = timezone.now()
        p = Product.objects.get(id=kwargs['pk'])
        if time_now < p.end and p.rent_status == False:
            form = BidsForm()
            context = {
                'name': p.name,
                'desp': p.desp,
                'start': p.start,
                'minbid': p.minimum_price,
                'end': p.end,
                'category': p.category,
                'currentbid': p.current_bid,
                'form': form,
                'id': p.id
            }
            return render(request, self.template_name, context)
        else:
            p.product_sold = True
            p.save()
            context = {
                'name': p.name,
                'desp': p.desp,
                'start': p.start,
                'minbid': p.minimum_price,
                'end': p.end,
                'category': p.category,
                'currentbid': p.current_bid,
                'buyer': p.bidder_id,
            }

            return render(request, 'app/product_sold.html', context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs["pk"])
        form = BidsForm(request.POST)
        if form.is_valid():
            product.bidder_id = request.user

            if product.bidder_id == product.seller_id:
                redirect('home')

            else:

                if product.minimum_price < int((request.POST['bidder_amount'])) and \
                        product.current_bid < int((request.POST['bidder_amount'])):
                    product.current_bid = int((request.POST['bidder_amount']))
                    product.save()

        context = {
            'name': product.name,
            'desp': product.desp,
            'start': product.start,
            'minbid': product.minimum_price,
            'end': product.end,
            'category': product.category,
            'currentbid': product.current_bid,
            'form': form
        }
        return render(request, self.template_name, context)


# ------------------USER CAN SEE WHAT ALL PRODUCTS HAVE BEEN LISTED FOR SALE-------------------------------------------


class ProductListed(View):

    template_name = 'app/product_listed.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user
        product = Product.objects.filter(seller_id=user_id)
        context = {
            'product': product
            }

        return render(request, self.template_name,context)


# ---------------------USER CAN SEE THE BIDS(LIVE) IN WHICH HE/SHE IS CURRENTLY WINNING---------------------------------


class BidsCurrentlyWinning(View):

    template_name = 'app/bids_currently_winning.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user
        product = Product.objects.filter(bidder_id=user_id, product_sold=False)
        context = {
            'product': product
        }

        return render(request, self.template_name, context)


# -------------------USER CAN VIEW ALL THE BIDS HE/SHE HAS WON TILL NOW------------------------------------------------


class BidsWon(View):
    template_name = 'app/bids_won.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user
        product = Product.objects.filter(bidder_id=user_id, product_sold=True)
        context = {
            'product': product
        }
        return render(request, self.template_name, context)


# ----------------------PRODUCTS AVAILABLE FOR RENT---------------------------------------------------------------------

class RentView(View):
    template_name = 'app/rent_view.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        rent_product_list = Product.objects.filter(current_bid=0)

        context = {
            'rent_product_list': rent_product_list,
        }

        return render(request, self.template_name, context)


#----------------------------RENT PRODUCT HERE--------------------------------------------------------------------------

class RentProductView(View):
    template_name = 'app/rent_products.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        rent_product = Product.objects.get(id=kwargs['pk'])
        if rent_product.rent_status == False:
            context = {
                'name': rent_product.name,
                'desp': rent_product.desp,
                'category': rent_product.category,
                'rent': rent_product.rent_price,
                'owner': rent_product.seller_id,
            }
            return render(request, self.template_name, context)

        else:

            context = {
                'name': rent_product.name,
                'desp': rent_product.desp,
                'category': rent_product.category,
                'rent': rent_product.rent_price,
                'owner': rent_product.seller_id,
                'temp_onwer': rent_product.rent_id
                      }

            return render(request, 'app/product_already_rented.html', context)


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        rent_product = Product.objects.get(id=kwargs['pk'])
        user_id = request.user
        rent = request.POST['rented']

        if rent_product.seller_id == user_id:
            redirect('home')

        else:
            if rent == 'product_rented':
                time_now = timezone.now()
                return_time = timezone.now() + timezone.timedelta(days=1)
                rent_product.save(commit=False)
                rent_product.rent_id = user_id
                rent_product.rent_status = True
                rent_product.rent_time_start = time_now
                rent_product.rent_time_end = return_time
                rent_product.save()

            return redirect('products_rented')


#------------------------------------PRODUCTS RENTED-------------------------------------------------------------------

class ProductsRented(View):
    template_name = 'app/products_rented.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user
        product = Product.objects.filter(rent_id=user_id)
        time_now = timezone.now()
        time_end = product.rent_time_end

        if time_now > time_end :
            product.save(commit=False)
            product.rent_fine = 10
            product.save()
        context = {
            'product': product
        }


        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return_product = Product.objects.get(id=kwargs['pk'])
        user_id = request.user
        return_pro = request.POST['return']
        if return_pro == 'return_product':
            return_product.rent_id = NULL
            return_product.rent_status = False
            return_product.save()

        return redirect('home')
