from django.shortcuts import get_object_or_404, redirect, render
from useraccounts.forms import UserProfileForm
from .forms import VendorForm

from useraccounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
# Create your views here.

def vendorProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    # by passing these instances inside the form, the form will load the existing content of this particular form
    
    # in case the user updates the form and clicks on submit
    # if request is post means that the user wants to store something inside the database
    if request.method =='POST':
        #  "request.FILES" represents any files uploaded by the user.
        #  "request.POST" represents data uploaded by the user.
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings updated')
            return redirect('vendorProfile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance = vendor)

    context ={
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vendorProfile.html',context)