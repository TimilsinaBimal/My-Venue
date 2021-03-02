from django.db import models
from django.conf import settings


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

    # def is_available(self, proposed_date) -> bool:
    #     if proposed_date not in self.date:
    #         return True
    #     else:
    #         return False


class Order(models.Model):
    order_id = models.CharField(max_length=255, verbose_name="Order ID")
    date = models.DateField(verbose_name="Ordered Date")
    name = models.ForeignKey(
        Venue, on_delete=models.CASCADE, verbose_name="Name of the Venue")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} on {self.date}"
