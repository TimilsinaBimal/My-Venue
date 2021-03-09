from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('venue/<venue_name>/<date>/', views.venue_detail, name="venue_detail"),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name="payment"),
    path('success/', views.success, name='success')

]
