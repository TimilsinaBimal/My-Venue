from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from .models import Venue, Order, Event, Payment
from .forms import CheckoutForm, PaymentForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import datetime
import random
import string
import stripe


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


def generate_order_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=12))


def delete_expired_orders(user):
    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        for order in order_qs:
            started_time = order.ordered_date
            present_time = timezone.now()
            if started_time < present_time - datetime.timedelta(minutes=5):
                order.delete()
                print("Deleted!")
    else:
        print("Not Found")


def get_seconds(ordered_date, limit=5):
    limit = limit * 60  # Converting to seconds
    seconds = timezone.now() - ordered_date
    return (limit - seconds.total_seconds())


def home(request):
    if not request.user.is_anonymous:
        delete_expired_orders(request.user)

    venues = Venue.objects.all()
    cities = [venue.city for venue in venues]
    context = {
        'cities': cities
    }
    return render(request, 'main/home.html', context)


def is_available_on(venue, date):
    results = Order.objects.filter(date_booked_for=date)
    venue_names = [result.venue_name for result in results]
    names = [venue.name for venue in venue_names]
    if venue in names:
        return False
    return True


@login_required
def search(request):
    delete_expired_orders(request.user)
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
    delete_expired_orders(request.user)
    return HttpResponse("WELCOME TO PROFILE")


@login_required
def venue_detail(request, venue_name, date):
    delete_expired_orders(request.user)
    venue = venue_name.replace('-', ' ')
    if is_available_on(venue, date):
        try:
            result = Venue.objects.get(name=venue)
        except Venue.DoesNotExist:
            raise Http404("ERROR 404 NOT FOUND!!")
        return render(
            request,
            'main/venue_details.html',
            {
                'venue': venue,
                'date': date,
                'result': result
            }
        )
    else:
        venue_object = Venue.objects.get(name=venue)
        result = Order.objects.get(
            venue_name=venue_object, date_booked_for=date)
        booked_user = result.user
        if booked_user == request.user:
            return redirect('checkout')
        else:
            raise Http404("Venue Not available for given date!!")


@login_required
def checkout(request):
    delete_expired_orders(request.user)
    events = Event.objects.all()
    events_name = [event.name for event in events]
    event_dict = dict()
    if request.method == "POST":
        venue = request.POST.get('venue')
        date = request.POST.get('date')
        for name in events_name:
            event_dict[name] = request.POST.get(name)

        result = Venue.objects.get(name=venue)

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
        form = CheckoutForm()
        context = {
            'result': result,
            'events': temp_events,
            'prices': prices,
            'total_price': total_price,
            'form': form,
        }
        order_qs = Order.objects.filter(
            date_booked_for=date, venue_name=result)
        if order_qs.exists():
            booked_user = order_qs[0].user
            if booked_user == request.user:
                if not order_qs[0].ordered:
                    if order_qs[0].user_phone_number == 0 and order_qs[0].user_address == "":
                        context.update(
                            {"seconds": get_seconds(order_qs[0].ordered_date)})
                        return render(request, 'main/checkout.html', context)
                    else:
                        return render(request, 'main/payment.html')
            else:
                return redirect("home")
        else:
            instance = Order.objects.create(
                order_id="",
                ordered_date=timezone.now(),
                venue_name=result,
                user=request.user,
                ordered=False,
                date_booked_for=date,
                confirmed=False,
                user_email=request.user.email,
                user_phone_number=0,
                user_address=""
            )
            for event in events:
                event_name = event.name
                if event_dict[event_name] == 'on':
                    instance.selected_events.add(
                        Event.objects.get(name=event_name))

            context.update({"seconds": get_seconds(instance.ordered_date)})
            return render(request, 'main/checkout.html', context)
    else:
        return redirect('home')


@login_required
def payment(request):
    delete_expired_orders(request.user)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if request.method == "POST":
            form = CheckoutForm(request.POST)
            if form.is_valid():
                default_full_name = request.POST.get('default_name')
                if default_full_name == "on":
                    full_name = f"{request.user.first_name} {request.user.last_name}"
                else:
                    full_name = form.cleaned_data.get('full_name')

                default_email = request.POST.get('default_email')
                if default_email == "on":
                    email = request.user.email
                else:
                    email = form.cleaned_data.get('email')

                phone_number = form.cleaned_data.get('phone_number')
                address = form.cleaned_data.get('address')

                if email == "":
                    messages.warning(request, "Email Field is required!")
                    return redirect(".")
                if full_name == "":
                    messages.warning(request, "Full name is required!")
                    return redirect(".")

                if address == "":
                    messages.warning(request, "Address is required!")
                    return redirect(".")

                if not phone_number:
                    messages.warning(request, "Phone number is required!")
                    return redirect(".")

                order.user_email = email
                order.user_full_name = full_name
                order.user_address = address
                order.user_phone_number = phone_number
                order.save()

                context = {
                    'order': order,
                    'form': PaymentForm,
                    'seconds': get_seconds(order.ordered_date)
                }
                return render(request, "main/payment.html", context)
            else:
                messages.error(
                    request, "Some error occured while filling the form. Please fill again")
                return redirect(".")
        else:
            return redirect("home")
    else:
        return redirect("home")


@login_required
def success(request):
    delete_expired_orders(request.user)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        context = {'order': order}
        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                token = form.cleaned_data.get('stripeToken')
                amount = int(order.get_total() * 100)
                try:
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token,
                        description=f"Booked Venue: \n {order.venue_name.name} with events {order.selected_events.all()}",
                    )

                    # Create Payment
                    payment = Payment()
                    payment.stripe_charge_id = charge['id']
                    payment.user = request.user
                    payment.amount = order.get_total()
                    payment.save()

                    order.ordered = True
                    order.order_id = generate_order_id()
                    order.confirmed = True
                    order.payment = payment
                    order.ordered_date = timezone.now()
                    order.save()
                    if order.confirmed:
                        message = f"Dear {order.user_full_name},\n Your request to book {order.venue_name.name} for {order.date_booked_for} is confirmed!\n If you want to cancel this order, please contact : (Number).\n Thank you for booking with us!"
                        subject = f"Order Confirmed for {order.venue_name.name}"
                        email = order.user_email
                        send_mail(subject, message, email, [
                            'timilsina.bml05@gmail.com'], fail_silently=False)
                        messages.success(
                            request, "You have successfully booked the venue! Thank you for Booking with us!")
                        return render(request, 'main/success.html')

                except stripe.error.CardError as e:
                    # Since it's a decline, stripe.error.CardError will be caught
                    messages.error(request, f"{e.error.message}")
                    return redirect('.', context)

                except stripe.error.RateLimitError as e:
                    # Too many requests made to the API too quickly
                    messages.error(
                        request, "ERROR! Too many requests made to the API quickly!")
                    return redirect('.', context)

                except stripe.error.InvalidRequestError as e:
                    # Invalid parameters were supplied to Stripe's API
                    messages.error(request, "ERROR! Invalid Parameters!")
                    return redirect('.', context)

                except stripe.error.AuthenticationError as e:
                    # Authentication with Stripe's API failed
                    # (maybe you changed API keys recently)
                    messages.error(request, "Authentication Error!")
                    return redirect('.', context)

                except stripe.error.APIConnectionError as e:
                    # Network communication with Stripe failed
                    messages.error(
                        request, "ERROR! Network Connection Failed!")
                    return redirect('.', context)

                except stripe.error.StripeError as e:
                    # Display a very generic error to the user, and maybe send
                    # yourself an email
                    messages.error(
                        request, "Something went wrong. You were not charged. Please try again later!")
                    return redirect('.', context)

                except Exception as e:
                    # Something else happened, completely unrelated to Stripe
                    messages.error(
                        request, f"A serious Error Occured! We have been notified!")
                    return redirect('.', context)
            messages.warning(request, "Invalid data received")
            return redirect(".", context)
    return redirect("payment")
