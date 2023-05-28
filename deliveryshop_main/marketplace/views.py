from django.shortcuts import render

from vendor.models import Vendor

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)
    count_vendor = vendors.count()
    #counter here
    context = {
        'vendors' : vendors,
        'count_vendor': count_vendor,
    }
    return render(request,'marketplace/listings.html',context)
