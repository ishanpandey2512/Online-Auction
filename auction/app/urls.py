from django.urls import path

from . import views

urlpatterns = [
    path('buyer/<int:pk>/', views.ProductView.as_view(), name='product'),
   # path('', views.IndexView.as_view(), name='index'),
    path('buyer/', views.BuyerView.as_view(), name='buyer')
]