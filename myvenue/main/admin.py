from django.contrib import admin
from .models import Venue, Event, Order, Payment
from django.db import models
from tinymce.widgets import TinyMCE
from django.contrib.auth.models import Group

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
    list_display = [
        'name',
        'city',
        'address',
        'price',
        'capacity'
    ]

    list_filter = [
        'city',
        'capacity',

    ]


class OrderAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        query = super(OrderAdmin, self).get_queryset(request)
        filtered_query = query.filter(ordered=True)
        return filtered_query

    fieldsets = [
        ("General Details", {"fields": ["order_id", "ordered_date"]}),
        ("Venue and Events", {"fields": [
         "venue_name", "selected_events", "date_booked_for"]}),
        ("User Details", {"fields": [
         "user", "user_full_name", "user_email", "user_phone_number", "user_address", "payment"]}),
        ("Confirmation", {"fields": ["ordered", "confirmed"]})
    ]
    list_display = [
        'order_id',
        'user',
        'venue_name',
        'date_booked_for',
        'confirmed'
    ]

    list_filter = [
        'date_booked_for',
        'user',
        'venue_name',
    ]


class PaymentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    list_display = [
        'stripe_charge_id',
        'user',
        'amount'
    ]

    list_filter = [
        'user'
    ]


class EventAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price'
    ]


admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)

admin.site.unregister(Group)
