from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime


class Event(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Name of the Event")
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of the Venue")
    email = models.CharField(max_length=255, verbose_name="Contact Email")
    phone_number = models.BigIntegerField(verbose_name="Contact Phone Number")
    capacity = models.IntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price of Venue")
    address = models.CharField(max_length=255, verbose_name="Address Line 1")
    city = models.CharField(max_length=255)
    street_number = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='venues/', verbose_name="Image of the venue")
    events = models.ManyToManyField(
        Event, default=None,  verbose_name="Events that can be organized")
    description = models.TextField(verbose_name="Description of the place")

    def __str__(self):
        return self.name

    def get_url(self):
        url = self.name.replace(' ', '-')
        return url


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2,
                                 max_digits=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    order_id = models.CharField(max_length=12, verbose_name="Order ID")
    ordered_date = models.DateTimeField(
        verbose_name="Ordered Date and Time")
    venue_name = models.ForeignKey(
        Venue, on_delete=models.CASCADE, verbose_name="Name of the Venue")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    selected_events = models.ManyToManyField(
        Event, verbose_name="Selected Events")
    ordered = models.BooleanField(default=False)
    date_booked_for = models.DateField(verbose_name="Date Booked for")
    confirmed = models.BooleanField(default=False)
    user_email = models.EmailField(verbose_name="User Email")
    user_phone_number = models.BigIntegerField(
        verbose_name="Contact Number of User")
    user_address = models.CharField(
        max_length=200, verbose_name="Address of User")
    user_full_name = models.CharField(
        max_length=150, verbose_name="Full name of User")
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.venue_name} on {self.date_booked_for}"

    def get_total(self):
        total_price = self.venue_name.price
        for event in self.selected_events.all():
            total_price += event.price
        return total_price
