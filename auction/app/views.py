
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect,render_to_response

from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, LoginForm, EditProfileForm

from django.contrib.auth.models import User
from django.contrib import messages

from django.views import generic
from django.utils.decorators import method_decorator

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail
from auction.settings import EMAIL_HOST_USER
from .models import MyProfile
from .forms import ProductForm
from .models import Product, Bids
from django.views.generic import DetailView,FormView,ListView
from django.views.generic.edit import FormMixin
from .forms import BidsForm
from django.views import View
from django.db.models import Q
from django.template import RequestContext


def home(request):
    return render(request, 'app/home.html')

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
            form = SignupForm()
        return render(request, 'app/signup.html', {'form': form})


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
                return render(request, 'app/home.html')
            else:
                return HttpResponse('Please! Verify your Email first')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')

    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})





@login_required
def profile_view(request):
    return render(request, 'app/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.myprofile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user.myprofile)
    return render(request, 'app/edit_profile.html', {'form': form})

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


class BuyerView(ListView):

    template_name = 'app/buyer.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.order_by('id')






class ProductView(View):

    template_name = 'app/product.html'

    def get(self, request, *args, **kwargs):

        p = Product.objects.get(id=kwargs['pk'])
        form = BidsForm()
        context = {
            'name': p.name,
            'desp': p.desp,
            'start': p.start,
            'minbid': p.minimum_price,
            'end': p.end_date,
            'category': p.category,
            'currentbid': p.current_bid,
            'form': form

        }

        if p.product_sold == 'False':
            return render(request, 'app/product_sold.html', context)
        else:
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        p = Product.objects.get(id=kwargs["pk"])
        print(p.name)
        form = BidsForm(request.POST)
        if form.is_valid():
            print(12)
            if p.minimum_price < int((request.POST['bidder_amount'])) and \
                    p.current_bid < int((request.POST['bidder_amount'])):
                p.current_bid = int((request.POST['bidder_amount']))
                print(p.current_bid)
                p.save()

        context = {
            'name': p.name,
            'desp': p.desp,
            'start': p.start,
            'minbid': p.minimum_price,
            'end': p.end_date,
            'category': p.category,
            'currentbid': p.current_bid,
            'form': form
            }

        return render(request, self.template_name, context)

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_item = form.save(commit=False)
            product_item.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'app/product_form.html', {'form' : form})




'''
def category_product(request):
    if request.method == "POST":
        form = categoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            
            return redirect('home')
    else:
        form = categoryForm()
    return render(request, 'app/category_search.html', {'form' : form})
'''
'''
def category_product(request):

    if request.method=="POST":
        item=request.POST['item']
        if item:
            match=Product.objects.filter(Q(name__icontains=item))
            if match:
                return render(request,'app/category_search.html',{'sr':match})

            else:
                messages.error(request,'no results')
        else:
            return HttpResponseRedirect('/category/')

    return render(request,'app/category_search.html',{'Product':Product})'''

def search_titles(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    product = Product.objects.filter(name__icontains=search_text)

    return render(request,'app/base1.html',{'product': product})
'''
def articles(request):
    language='en-gb'
    session_language='en-gb'

    if 'lang' in request.COOKIES:
        language=request.COOKIES['lang']
    if 'lang' in request.session:
        session_language=request.session['lang']
    args={}
    args.update(csrf(request))
    args['articles']=Product.objects.all()
    args[language]=language
    args['session_language']=session_language
    return render_to_response('app/base1.html',args)'''

