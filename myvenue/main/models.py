from django.db import models


# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of the Venue"),
    email = models.EmailField(),
    phone_number = models.BigIntegerField(),
    capacity = models.IntegerField(),
    location = models.CharField(),
    image = models.ImageField(upload_to='venues/')

