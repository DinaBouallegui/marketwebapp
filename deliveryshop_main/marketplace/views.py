from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from menu.models import Category, FoodItem

from vendor.models import Vendor
from django.db.models import Prefetch

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
    # prefetch related will look for the data in a reverse manner
    # because there is no food item foreign key in category model but want to get the food items that
    # belong to one category
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        #make query inside the prefetch
        Prefetch(
        'fooditems',
        queryset= FoodItem.objects.filter(is_available=True)
        )
    )

    context = {
        'vendor': vendor,
        'categories' : categories,
    }
    return render(request,'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id=None):
    return HttpResponse('Testing')