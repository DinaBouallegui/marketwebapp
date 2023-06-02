from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

def place_order(request):
    return render(request,'orders/place_order.html')