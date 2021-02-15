from django.db import models


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
    events = models.TextField(verbose_name="Events that can be organized")
    description = models.TextField(verbose_name="Description of the place")

    def __str__(self):
        return self.name
