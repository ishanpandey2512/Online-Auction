
from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', views.Home.as_view(), name='home'),
    re_path(r'^signup/$', views.SignUp.as_view(), name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.Activate.as_view(), name='activate'),
    re_path(r'^login/$', views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    re_path(r'^profile/(?P<user_id>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    re_path(r'^profile/(?P<user_id>[0-9]+)/edit/$', views.ProfileEdit.as_view(), name='edit_profile'),
    re_path('seller/', views.AddProduct.as_view(), name='add_product'),
    path('buyer/<int:pk>/', views.ProductView.as_view(), name='product'),
    path('buyer/', views.BuyerView.as_view(), name='buyer'),
    path('product_listed/', views.ProductListed.as_view(), name='product_listed'),
    path('bids_currently_winning/', views.BidsCurrentlyWinning.as_view(), name='bids_currently_winning'),
    path('bids_won/', views.BidsWon.as_view(), name='bids_won'),
    re_path(r'^ajax/search/$', views.search, name='search'),
    url(r'^ajax/options/$', views.options, name='options')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)