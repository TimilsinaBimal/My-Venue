from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('venue/<venue_name>/', views.venue_detail, name="venue_detail"),
    path('checkout/<venue_name>/', views.checkout, name='checkout'),

]
