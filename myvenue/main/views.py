from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return HttpResponse("Bimal")


def profile(request):
    return HttpResponse("WELCOME TO PROFILE")