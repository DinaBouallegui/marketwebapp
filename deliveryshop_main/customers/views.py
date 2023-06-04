from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from orders.models import Order
# importing the user form
from useraccounts.forms import UserProfileForm,UserInfoForm
from django.contrib.auth.decorators import login_required
from useraccounts.models import UserProfile



# Create your views here.
# create a function for profile

@login_required(login_url='login')
def customerprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        #request.Files because of storing of the photos
        profile_form = UserProfileForm(request.POST,request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            #save both of the forms
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile updated')
            return redirect('customerprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context ={
        'profile_form' : profile_form,
        'user_form': user_form,
        'profile': profile,
    }
    return render(request,'customers/customerprofile.html',context)

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered = True)
    context ={
        'orders':orders,
    }
    return render(request, 'customers/my_orders.html',context)