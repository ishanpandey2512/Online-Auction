from django.db import models
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .forms import ContactForm, LoginForm

from django.core.mail import send_mail
from auction import *

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from .forms import SignupForm
from django.contrib.auth.forms import User, UserCreationForm
from django.views.generic import View
from django.views.generic.edit import FormView
from .forms import *
from .models import *
# Create your views here.

class Signup(FormView):
    form_class  = ContactForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        try:
            form = self.form_class
            # inside request.session is a variable which is dict-like object.
            # to use request, add 'django.core.context_processors.request' to TEMPLATE_CONTEXT_PROCESSORS.
            if (request.session['inSession'] is False or None):
                return render(request, self.template_name, {'form': form})
            else:
                return HttpResponseRedirect(reverse('index'))
        except KeyError:
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class[request.POST]       # INSTANCE OF SUBMITTED POST FORM.

        # firstly, check if form is valid
        # otherwise, redirect it to signup page with errors.

        if form.is_valid():
            pass
        else:
            # display messages if any, or, redirect it


            # to the referer view of current request.
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return HttpResponseRedirect('registration/signup.html')

        # if form is valid, new person is created, but not saved, since commit=false
        new_Person = form.save(commit=False)

        # retrieving all objects that exist in db, to find out if email already exists.
        # if that email does not exist, then a email verification is sent.
        try:
            if_email = Person.objects.get(email=new_Person.email)
            except Person.DoesNotExist:
            try:
                    if_username = Person.objects.get(userName = Person.userName)
                    except Person.DoesNotExist:
                    new_Person.save()
                    try:
                                    #EmailMessage can also be used.
                                    #params of send_mail: context, message, from, recipient_list, fail_silently, auth_user, auth_password, connection, html_meassage.
                                    #fail_silently = False -> raises error from SMTPLib
                                    #fail_silently = True -> no error if email isn't sent successfully, its for beginners.
                                    send_mail("Registration successful",
                                              "Now, Enjoy our services by Signing-In",
                                              settings.EMAIL_HOST_USER,
                                              [new_Person.email],
                                              fail_silently= True,
                                              html_message="<p><i>You have successfully registered.</i></p>",
                                               )
                    except:
                        pass
                        #some message
                        #redirecting to index as it is our profile page.
                        return HttpResponseRedirect(reverse('app:index'))
            else:
#unsuccessful signup due to username already exists.
                return HttpResponseRedirect(reverse('app: signup'))
        else:
# unsuccessful signup due to email already exists.
        return HttpResponseRedirect(reverse('app:signup'))

class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect('/form')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

        return render(request, "index.html")



class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)







