from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserForm
from django.shortcuts import redirect
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # #storing the password in a hashed format
            # password = form.cleaned_data['password']
            # #before saving this user it should assign the role to this user commit =False (this form is ready to be saved)
            # user = form.save(commit = False)
            # user.set_password(password)
            # #i will assign the role to the user either customer or restaurant
            # user.role = User.CUSTOMER
            # #saving this user
            # form.save()
            # #here it's triggering the signal
            # return redirect('registerUser')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name ,last_name = last_name,username= username,email=email,password= password)
            user.role = User.CUSTOMER
            #saving the user to the database
            user.save()
            print('User is created')
            #displaying a message after the user registration
            messages.success(request, 'Your account has been registered successfully!')
            #redirecting the user to registerUser page again
            return redirect('registerUser')
        else: 
            print('invalid form')
            print(form.errors)
    else: 
        form= UserForm()
    # we will padd this user form() inside register user.html
    context = { 
        'form' : form,
    }
    return render(request,'useraccounts/registerUser.html', context)

def registerVendor(request):
    # if it's a post request/means if user clicked on submit

    if request.method == 'POST':
        # storing the data 
        #passing the content from the post request
        form = UserForm(request.POST)
        #vendor license is a file so request.post only contains char field and if the form has files you recieve them using request.Files
        v_form = VendorForm(request.POST,request.FILES)
        #if both of the forms are valid you can create the user ect
        if form.is_valid() and v_form.is_valid: 
            #creating the user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name ,last_name = last_name,username= username,email=email,password= password)
            user.role = User.VENDOR
            user.save() 
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,'Congratulations! Your account has been registered successfully! Wait for approval')
        else: 
            print('invalid form')
            print(form.errors)
     
    #else if it's a get request
    else:
        form = UserForm()
        v_form = VendorForm()
    
    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request,'useraccounts/registerVendor.html',context)