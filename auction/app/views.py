from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from .forms import SignupForm, LoginForm, EditProfileForm

from django.contrib.auth.models import User
from django.contrib import messages

from django.utils.decorators import method_decorator

from django.contrib.sites.shortcuts import get_current_site
from django.utils import dateparse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail
from auction.settings import EMAIL_HOST_USER

from .forms import ProductForm, VisaForm
from .models import Product

from django.views.generic import FormView
from .forms import BidsForm
from django.views import View
from .models import MyProfile


class Home(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context={
            # left empty for adding products currently in auction

        }
        return render(request, 'app/home.html')


def search(request):
    print("inside ajax")
    text = request.GET.get("value", "")
    k = Product.objects.filter(category__istartswith=text).values_list('name','id')

    data = {}
    data['products'] = list(k)

    return JsonResponse(data)
#
# def index(request):
#     return render(request, 'app/home.html')





# Signup using Email Verification
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


# account activation class

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


class LogoutView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been successfully Logged Out!!')
        return redirect('home')


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



class ProfileView(View):
    model = User
    @method_decorator(login_required)
    def get(self, request, user_id, *args, **kwargs):
        user_object = User.objects.get(id=user_id)
        # user_id in urls.py
        context = {
            "user": user_object
        }
        return render(request, 'app/profile.html', context)


class ProfileEdit(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # resolving no_reverse_match error
        user_obj = request.user.id
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.myprofile)
        if form.is_valid():
            form.save()
            # return redirect('home')
            # if user has successfully edited form, redirect him to edit profile view
            # so that user can view his current changes directly, using "namespacing" in urls, and redirecting.
            return redirect('profile', user_obj)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = EditProfileForm(instance= request.user.myprofile)
        context = {
            "form": form,
        }
        return render(request, 'app/edit_profile.html', context)

# -------------using generic views-------------------------------------------------------------------------------
class VisaForm(FormView):
    form_class = VisaForm
    template_name = 'app/visa.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            form = self.form_class
            current_user = request.user.id

            # using queryset, Visa model -> so, visa_set.
            # verifying if user already has a visacard in database
            context = {
                "form": form,
                "first_name": MyProfile.first_name,
                # as in models.
                "occurrence": occurrence,
            }
            if current_user.visa_set.count() == 0:
                return render(request, self.template_name, context)
            else:
                return render(request, self.template_name, context)

        except:
            return HttpResponseRedirect(reverse('VisaForm'))

    def post(self, request, *args, **kwargs):
        try:
            current_user = request.user.id
            try:
                expDate = dateparse.parse_date(request.POST['exp_date'])
                if(expDate.today() > expDate):
                    return  HttpResponse("Visa has already expired")
            except ValueError:
                messages.error(request, "Enter correct Date")
                return HttpResponseRedirect(reverse('VisaForm'))
            #create applies database changes for all types of fields immediately.
            current_user.visa_set.create(visaNum=request.POST['visa_card_number'], expDate=request.POST['exp_date'])
            messages.success(request, "Visa has been registered successfully")
            return HttpResponseRedirect(reverse('home'))

        except MyProfile.DoesNotExist:
            messages.error(request, "You are not logged in.")
            return HttpResponseRedirect(reverse('login'))


# ---------------------------------------------------------------------------------------------
class AddProduct(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        # p = Product.objects.get(id=request.User.id)

        if form.is_valid():
            # product_item = form.save(commit=False).....WTF?
            product_item = form.save(commit=False)
            product_item.seller_id = request.user
            product_item.save()
            return redirect('home')
        else:
            return HttpResponse("form invalid")

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = ProductForm()
        context = {'form' : form}
        return render(request, 'app/product_form.html', context)

# ---------------------------------------------------------------------------------------------------


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


class ProductView(View):

    template_name = 'app/product.html'

    @method_decorator(login_required)
    def get(self, request,*args,**kwargs):
        time_now = timezone.now()
        p = Product.objects.get(id=kwargs['pk'])
        if time_now < p.end:
            form = BidsForm()
            context = {
                # 'image': p.image,
                'name': p.name,
                'desp': p.desp,
                'start': p.start,
                'minbid': p.minimum_price,
                'end': p.end,
                'category': p.category,
                'currentbid': p.current_bid,
                'form': form
            }
            return render(request, self.template_name, context)
        else:
            context = {
                # 'image': p.image,
                'name': p.name,
                'desp': p.desp,
                'start': p.start,
                'minbid': p.minimum_price,
                'end': p.end,
                'category': p.category,
                'currentbid': p.current_bid,
                'buyer': p.bidder_id,
            }
            # p.product_sold = "TRUE"
            # p.save()
            return render(request, 'app/product_sold.html', context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # user_obj = request.user.id
        p = Product.objects.get(id=kwargs["pk"])
        # b = Bids.objects.get(id=user_obj)

        form = BidsForm(request.POST)
        if form.is_valid():

            p.bidder_id = request.user

            if p.bidder_id == p.seller_id:
                return redirect('home')

            else:

                if p.minimum_price < int((request.POST['bidder_amount'])) and \
                        p.current_bid < int((request.POST['bidder_amount'])):
                    p.current_bid = int((request.POST['bidder_amount']))
                    p.save()

        context = {
            'image': p.image,
            'name': p.name,
            'desp': p.desp,
            'start': p.start,
            'minbid': p.minimum_price,
            'end': p.end,
            'category': p.category,
            'currentbid': p.current_bid,
            'form': form
        }
        return render(request, self.template_name, context)


class ProductListed(View):

    template_name = 'app/product_listed.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user
        pr = Product.objects.filter(seller_id=user_id)
        context = {
            'product': pr
            }

        return render(request, self.template_name,context)


class BidsCurrentlyWinning(View):

    template_name = 'app/bids_currently_winning.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user
        pr = Product.objects.filter(bidder_id=user_id)
        context = {
            'product': pr
        }

        return render(request, self.template_name, context)


class BidsWon(View):
    template_name = 'app/bids_won.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user
        pr = Product.objects.filter(bidder_id=user_id, product_sold=True)
        context = {
            'product': pr
        }
        return render(request, self.template_name, context)




