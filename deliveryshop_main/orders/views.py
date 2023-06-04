from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from marketplace.context_processors import get_cart_amounts
from marketplace.models import Cart
from .models import Order, OrderedFood, Payment
from .forms import OrderForm
import simplejson as json
from .utils import generate_order_number

# Create your views here.
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('marketplace')
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    print(tax_data)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            #assigning the user here
            order.user = request.user
            #payment to update
            #total update here
            order.total = grand_total
            # tax data update here  
            order.tax_data = json.dumps(tax_data)
            # total taxupdate here  
            order.total_tax = total_tax
            order.payment_method = request.POST['payment-method']
            # status by default its new
            # is_ordered by default its false, don't need to put it 
            # created_at / updated_at will be automatically updated
            #order_number update here 
            order.save() # here the pk or order id is generated
            order.order_number = generate_order_number(order.id)
            order.save() # once generated, should save again
            context = { 
                'order': order,
                'cart_items': cart_items,
            }
            return render(request,'orders/place_order.html',context)  
        else:
            print(form.errors)
    return render(request,'orders/place_order.html')


def payments(request):
        #checking if the request is ajax or not 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # storing the payment details in the payment model
        # order number coming from ajax which is in request.post
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order = Order.objects.get(user=request.user, order_number= order_number)
        # create payment object
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()
        # update the order model 
        order.payment = payment
        order.is_ordered = True
        order.save()
        # move the cart items to ordered food model
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity #this is the total amount 
            ordered_food.save() 
        return HttpResponse('save ordered food')

        # send order confirmation email to the customer 

        # send order received email to the vendor

        # clear the cart if the pamyment is successfull 

        # return back to ajax with the status success or failure

    return HttpResponse('Payments view')