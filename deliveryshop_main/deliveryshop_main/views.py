from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hi this is the main page!")

def about(request):
    return HttpResponse("This is about section")