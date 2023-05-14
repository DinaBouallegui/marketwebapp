from base64 import urlsafe_b64decode
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserForm
from django.shortcuts import redirect
from .models import User, UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorForm
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor


# Create your views here.

#custom decorate is here and 
# Restricting the Vendor/Restaurant from accessing the customer page

def check_role_vendor(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied


def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


#Restricting the customer from accessing the vendor page

def registerUser(request):

    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('dashboard')
    
    elif request.method == 'POST':
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
            # we send a verification email right after we save the user 
            #helper function that send the verification email
            send_verification_email(request,user)

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
            #here sending the verification email
            send_verification_email(request,user)
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

def login(request):

    # if the use is already logged in and tried to log in again
    if request.user.is_authenticated:
        messages.warning (request,'You are already logged in')
        # redirect him to the dashboard page
        return redirect('myAccount')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
      # the authenticate function will take the email and password and will return the user to whom this email and password belongs to
        user = auth.authenticate(email = email, password = password)
        #if we can get the user we can just log in
        if user is not None:
            #login() is a function of auth package and it will allow to log him in
            auth.login(request, user)
            messages.success(request,'You are now logged in.')
            # if the user is logged in he is redirected to the dashboard
            return redirect('myAccount')
        else:
            messages.error(request,'The login credentials are invalid')
            #it will redirect to the login page
            return redirect('login')
    return render(request,'useraccounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'Now you are logged out :( ')
    return redirect('login')

#function that decides whether the person who is logging in is a customer or a vendor
#if you're not logged in you're not supported to enter to this view
#if the user is not logged it and tries to access useraccounts/myAccount he will be send to login page

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

# same thing customer dashborad should only be accessible when the user is logged in
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request): 
    return render(request,'useraccounts/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request): 
    #function for fetching the user's  profile details 
    # request.user -> only the logged in user can enter inside this view 
    #vendor = Vendor.objects.get(user= request.user)
    #context = { 
     #   'vendor': vendor, 
    #}
    #return render(request,'useraccounts/vendorDashboard.html', context )
    return render(request,'useraccounts/vendorDashboard.html')
    # we can access vendor object only inside  useraccounts/vendorDashboard page for now
    #I need access of the vendor object from every html page 
    # this is possible using the concept of context processor => will give access to theobject inside every html page
    # context processor is a function that takes only one argument which is request 
    # -> return a dictionary that gets added to the request context -> this dictionary can be accessed ine very html page



def activate(request, uidb64, token):
    #Activate the user by setting the is_active status to True
    try: 
        uid = urlsafe_b64decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
        #making sure it's the correct token for that user
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratss! Just activated your account.')
        return redirect('myAccount')
        #myAccount will check to redirect him to which dashboard
    else: 
        messages.error(request,'Invalid activation link')
        return redirect('myAccount')