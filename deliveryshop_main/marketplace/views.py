import traceback
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from useraccounts.models import UserProfile

from .context_processors import get_cart_amounts, get_cart_counter
from .models import Cart
from menu.models import Category, FoodItem

from orders.forms import OrderForm
from vendor.models import Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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
    # query to get the cart items: 
    if request.user.is_authenticated: 
        cart_items = Cart.objects.filter(user=request.user)
    else: 
        cart_items = None
    context = {
        'vendor': vendor,
        'categories' : categories,
        'cart_items': cart_items,
    }
    return render(request,'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id):
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
                        return JsonResponse({'status': 'Success', 'message': 'The cart quantity increased','cart_counter': get_cart_counter(request), 'qty': check_cart.quantity,'cart_amount': get_cart_amounts(request) })
                        # If the user didn't add that product to the cart
                    except:
                        # Create a new cart entry
                        check_cart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                        return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart','cart_counter': get_cart_counter(request),'qty': check_cart.quantity,'cart_amount': get_cart_amounts(request) })
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'This Food Item does not exist'})
            else:
                # The request must be AJAX
                return JsonResponse({'status': 'Failed', 'message': 'The request is invalid!'})
        # It will be sent to the user when they're not logged in
        else:
            return JsonResponse({'status': 'login_required', 'message': 'No no no :(( Please login to continue'})
  
    
    
def decrease_cart(request,food_id): 
        # Your code goes here.
        # Adding the logic for deleting a product to the cart
        if request.user.is_authenticated:
        # Checking if the request is also Ajax
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Checking if the food item exists
                try:
                    fooditem = FoodItem.objects.get(id=food_id)
                    # Checking if the user has already added that food item to the cart
                    try:
                        check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                        # If the user has already added this particular item, decrease the quantity
                        if check_cart.quantity > 1: 
                            check_cart.quantity -= 1
                            check_cart.save()   
                        else: 
                            check_cart.delete()
                            check_cart.quantity = 0                     
                        return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': check_cart.quantity, 'cart_amount': get_cart_amounts(request)})
                        # If the user didn't add that product to the cart
                    except:
                        return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!' })
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'This Food Item does not exist'})
            else:
                # The request must be AJAX
                return JsonResponse({'status': 'Failed', 'message': 'The request is invalid!'})
        # It will be sent to the user when they're not logged in
        else:
            return JsonResponse({'status': 'login_required', 'message': 'No no no :(( Please login to continue'})

@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request,'marketplace/cart.html', context)

def delete_cart(request,cart_id): 
    # it will be handled with ajax request
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try: 
                # check if the cart item exists
                cart_item = Cart.objects.get(user= request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'The cart item was deleted', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except: 
                return JsonResponse({'status': 'Failed', 'message': 'This  Cart Item does not exist, you cannot delete'}) 
        else: 
            return JsonResponse({'status': 'Failed', 'message': 'The request is invalid!'})

def search(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']
    #print(address,latitude,longitude,radius)

    # get vendor ids that has the food item the user is looking for
    # we get the food items that matches with the keywords
    fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
   
   # Q object because i want to filter these data with or condition for complex queries 
   # Q query comes gfrom django db model
    vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
    # match with the restauran name, user approved should be true and user shoul be active
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count' : vendor_count,
    }

    # whenevr someone clicks on search button it goes to market place page
    return render(request,'marketplace/listings.html', context)


#users should be logged in
@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('marketpalce')
    
    # whatever data there is in the order model will be prepopulated in this form
    # assign the value of the logged in user to this order form
    # form = OrderForm(initial={'first_name':'Rathan'})
    user_profile = UserProfile.objects.get(user=request.user)
    #initial values 
    #when the form is empty, it renders the default values
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email':request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pincode,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request,'marketplace/checkout.html',context)