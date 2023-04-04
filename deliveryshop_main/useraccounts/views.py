from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserForm
from django.shortcuts import redirect
from .models import User
from django.contrib import messages

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
