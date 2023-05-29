from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Cart
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

def add_to_cart(request, food_id):
    try:
        # Your code goes here.
        # Adding the logic for adding a product to the cart
        if request.user.is_authenticated:
        # Checking if the request is also Ajax
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Checking if the food item exists
                try:
                    fooditem = FoodItem.objects.get(id=food_id)
                    # Checking if the user has already added that food item to the cart
                    try:
                        check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                        # If the user has already added this particular item, increase the quantity
                        check_cart.quantity += 1
                        check_cart.save()
                        return JsonResponse({'status': 'Success', 'message': 'The cart quantity increased'})
                        # If the user didn't add that product to the cart
                    except:
                        # Create a new cart entry
                        check_cart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                        return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart'})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'This Food Item does not exist'})
            else:
                # The request must be AJAX
                return JsonResponse({'status': 'Failed', 'message': 'The request is invalid!'})
        # It will be sent to the user when they're not logged in
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Please log in to continue'})
    except Exception as e:
            if request.is_ajax():
                return JsonResponse({'status': 'Failed', 'message': 'Unexpected error occurred: {}'.format(e), 'traceback': traceback.format_exc()}, status=500)
            else:
                raise e
    
    
