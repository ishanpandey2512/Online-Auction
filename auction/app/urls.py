
from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),

    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.Activate.as_view(), name='activate'),

    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    url(r'^profile/(?P<user_id>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<user_id>[0-9]+)/edit/$', views.ProfileEdit.as_view(), name='edit_profile'),
    url('seller/', views.AddProduct.as_view(), name='add_product'),

    path('VisaForm/', views.VisaForm.as_view(), name='VisaForm'),

    path('buyer/<int:pk>/', views.ProductView.as_view(), name='product'),
    path('buyer/', views.BuyerView.as_view(), name='buyer'),
    # path('buyer/<int:pk>/sold',views.ProductSold.as_view(), name='sold')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



