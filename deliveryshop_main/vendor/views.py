from django.shortcuts import get_object_or_404, render
from useraccounts.forms import UserProfileForm
from .forms import VendorForm

from useraccounts.models import UserProfile
from .models import Vendor
# Create your views here.

def vendorProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    # by passing these instances inside the form, the form will load the existing content of this particular form

    profile_form = UserProfileForm(instance = profile)
    vendor_form = VendorForm(instance = vendor)
    context ={
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vendorProfile.html',context)