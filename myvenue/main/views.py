from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import Event, Venue, Order
import datetime


# Create your views here.
def home(request):
    context = {}
    return render(request, 'main/home.html', context)


def is_available_on(venue, date):
    results = Order.objects.filter(date=date)
    venue_names = [result.name for result in results]
    names = [venue.name for venue in venue_names]
    if venue in names:
        return False
    return True


@login_required
def search(request):
    date = request.GET.get('date')
    city = request.GET.get('city')
    results = Venue.objects.filter(city=city)
    result_venues = [result.name for result in results]
    date_object = datetime.datetime.strptime(date, "%d %b %Y").date()
    final_results = []
    for idx, venue in enumerate(result_venues):
        if is_available_on(venue, date_object):
            final_results.append(results[idx])

    context = {
        'results': final_results,
        'date': date_object,
        'city': city
    }
    return render(request, 'main/search_results.html', context)


@login_required
def profile(request):
    return HttpResponse("WELCOME TO PROFILE")


@login_required
def venue_detail(request, venue_name):
    venue = venue_name.replace('-', ' ')
    try:
        result = Venue.objects.get(name=venue)
    except Venue.DoesNotExist:
        raise Http404("ERROR 404 NOT FOUND!!")
    events = result.events.all()
    events_name = [event.name for event in events]

    if request.method == "POST":
        for name in events_name:
            name = request.POST.get(name)
            print(name)
    context = {
        'result': result
    }
    return render(request, 'main/venue_details.html', context)


@login_required
def checkout(request, venue_name):
    venue = venue_name.replace('-', ' ')
    try:
        result = Venue.objects.get(name=venue)
    except Venue.DoesNotExist:
        raise Http404("ERROR 404 NOT FOUND!!")
    events = result.events.all()
    # events_name = {event.name for event in events}
    events_name = [event.name for event in events]
    event_dict = dict()
    if request.method == "POST":
        for name in events_name:
            event_dict[name] = request.POST.get(name)

    # Calculating Total Price after adding price of Extra Events
    base_price = result.price
    total_price = base_price
    temp_events = ['Basic']
    prices = [base_price]
    for event in events:
        if event_dict[event.name] == 'on':
            total_price += event.price
            temp_events.append(event.name)
            prices.append(event.price)

    context = {
        'result': result,
        'events': temp_events,
        'prices': prices,
        'total_price': total_price
    }
    return render(request, 'main/checkout.html', context)
