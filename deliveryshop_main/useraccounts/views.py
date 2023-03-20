from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserForm

# Create your views here.
def registerUser(request):
    form = UserForm()
    # we will padd this user form() inside register user.html
    context = { 
        'form' : form,
    }
    return render(request,'useraccounts/registerUser.html', context)
