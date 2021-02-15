from django.contrib import admin
from .models import Venue
from django.db import models
from tinymce.widgets import TinyMCE

# Register your models here.


class VenueAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Contact Information", {
         "fields": ["name", "email", "phone_number"]}),
        ("Address Details", {"fields": ["city", "street_number", "address"]}),
        ("Pricing and Capacity", {"fields": ["price", "capacity"]}),
        ("More Details", {"fields": ["image", "events", "description"]})

    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


admin.site.register(Venue, VenueAdmin)
