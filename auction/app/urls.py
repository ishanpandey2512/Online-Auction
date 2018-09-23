
from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r'^$', views.home, name='home'),

    path(r'^signup/$', views.signup, name='signup'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

    path(r'^login/$', views.login_view, name='login'),
    path(r'^logout/$', views.logout_view, name='logout'),

    path(r'^profile/$', views.profile_view, name='profile'),
    path(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    path('seller/', views.add_product, name='add_product'),

    # path(r'^VisaForm/$', views.VisaForm.as_view(), name='VisaForm'),

    path('buyer/<int:pk>/', views.ProductView.as_view(), name='product'),
    path('buyer/', views.BuyerView.as_view(), name='buyer')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



