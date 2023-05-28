from django.shortcuts import get_object_or_404, render

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

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug= vendor_slug)

    context = {
        'vendor': vendor,
    }
    return render(request,'marketplace/vendor_detail.html', context)
